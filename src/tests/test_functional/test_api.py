from copy import deepcopy
from http import HTTPStatus
from unittest.mock import patch

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from hamcrest import (
    assert_that,
    only_contains,
    has_entries,
    instance_of,
    all_of,
    has_length,
    greater_than,
)
from peewee import fn

from models.pages import Page, Block
from server import init


page_short_matcher = {
    "name": instance_of(str),
    "ordering": instance_of(int),
    "url": instance_of(str),
}
block_short_matcher = {
    "name": instance_of(str),
    "ordering": instance_of(int),
}
block_detail_matcher = {
    **block_short_matcher,
    "video_url": instance_of(str),
    "views": instance_of(int),
    "increment_url": instance_of(str),
}


class TestAPI(AioHTTPTestCase):
    """
    Requires imported backup.sql dump
    """

    @unittest_run_loop
    async def test_page_list(self):
        url = str(self.app.router["pages-list"].url_for())
        response = await self.client.get(url)
        assert response.status == HTTPStatus.OK
        content = await response.json()
        assert len(content) == Page.select().count() > 0
        page_matcher = deepcopy(page_short_matcher)
        page_matcher["blocks"] = all_of(
            has_length(greater_than(0)),
            only_contains(has_entries(block_short_matcher)),
        )
        assert_that(
            content,
            only_contains(has_entries(page_matcher)),
        )

    @unittest_run_loop
    async def test_page_detail_success(self):
        page = Page.select().first()
        url = str(self.app.router["pages-detail"].url_for(slug=page.slug))
        response = await self.client.get(url)
        assert response.status == HTTPStatus.OK
        content = await response.json()
        blocks_count = page.blocks.count()
        page_matcher = deepcopy(page_short_matcher)
        page_matcher["name"] = Page.name
        page_matcher["ordering"] = Page.ordering
        page_matcher["url"] = url
        page_matcher["blocks"] = all_of(
            has_length(blocks_count),
            only_contains(has_entries(block_detail_matcher)),
        )
        assert_that(
            content,
            has_entries(page_matcher),
        )

    @unittest_run_loop
    async def test_page_detail_not_found(self):
        url = str(self.app.router["pages-detail"].url_for(slug="slug_does_not_exists"))
        response = await self.client.get(url)
        assert response.status == HTTPStatus.NOT_FOUND

    @unittest_run_loop
    async def test_block_viewed_success(self):
        with patch.object(Block, "increment_views") as mock:
            block = Block.select().first()
            url = str(self.app.router["block-viewed"].url_for(id=str(block.id)))
            response = await self.client.patch(url)
            assert response.status == HTTPStatus.OK
            mock.assert_called_once()
            content = await response.json()
            assert_that(
                content,
                has_entries(block_detail_matcher),
            )

    @unittest_run_loop
    async def test_block_viewed_not_found(self):
        max_id = Block.select(fn.MAX(Block.id)).scalar()
        url = str(self.app.router["block-viewed"].url_for(id=str(max_id + 1)))
        response = await self.client.patch(url)
        assert response.status == HTTPStatus.NOT_FOUND

    async def get_application(self):
        app, host, port = await init()
        return app
