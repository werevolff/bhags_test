from aiohttp import web

from models.connection import objects
from models.pages import Page, Block
from serializers.pages import PageListSchema, PageDetailSchema, BlockDetailSchema
from .routes import routes


def setup_pages_routes(app: web.Application) -> None:
    app.router.add_routes(routes)


@routes.get("/pages", name="pages-list")
async def page_list(request: web.Request) -> web.json_response:
    pages = await objects.execute(Page.select())
    return get_json_response(PageListSchema, request, pages, many=True)


@routes.get(r"/pages/{slug:[a-z0-9\-]+}", name="pages-detail")
async def page_detail(request: web.Request) -> web.json_response:
    try:
        page = await objects.get(Page, slug=request.match_info["slug"])
    except Page.DoesNotExist:
        raise web.HTTPNotFound
    return get_json_response(PageDetailSchema, request, page)


@routes.patch(r"/pages/blocks/{id:\d+}/viewed", name="block-viewed")
async def set_block_viewed(request: web.Request) -> web.json_response:
    try:
        block = await objects.get(Block, id=request.match_info["id"])
    except Block.DoesNotExist:
        raise web.HTTPNotFound
    await block.increment_views()
    return get_json_response(BlockDetailSchema, request, block)


def get_json_response(schema_class, request, dump_data, **kwargs):
    schema = schema_class(**kwargs)
    schema.context["request"] = request
    data = schema.dump(dump_data)
    return web.json_response(data)
