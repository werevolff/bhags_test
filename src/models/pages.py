from peewee import Model, CharField, IntegerField, ManyToManyField
from slugify import slugify

from .connection import database, objects


class OrderingModelMixin:
    """
    Contains a method for refreshing an object's ordering
    field from the database
    """

    @property
    def ordering(self):
        raise NotImplementedError

    @classmethod
    def create(cls, *args, **kwargs):
        instance = super().create(*args, **kwargs)
        instance.refresh_ordering()
        return instance

    def refresh_ordering(self):
        # I've moved the ordering auto-incrementation to the database layer,
        # so we need to update the value after the instance is created.
        model_class = type(self)
        self.ordering = (
            model_class.select(model_class.ordering)
            .where(self._pk_expr())
            .get()
            .ordering
        )


class Block(OrderingModelMixin, Model):
    name = CharField(max_length=1000)
    video_url = CharField(max_length=1000, unique=True)
    ordering = IntegerField(sequence="block_ordering_seq")
    views = IntegerField(default=0)

    class Meta:
        database = database

    async def increment_views(self) -> None:
        async with objects.atomic():
            await objects.execute(
                Block.select(Block.views).for_update().where(self._pk_expr()),
            )
            self.views = await objects.scalar(
                Block.update(views=Block.views + 1)
                .where(self._pk_expr())
                .returning(Block.views),
            )


class Page(OrderingModelMixin, Model):
    name = CharField(max_length=1000, unique=True)
    slug = CharField(max_length=1000, unique=True)
    ordering = IntegerField(sequence="page_ordering_seq")
    blocks = ManyToManyField(Block, backref="pages", on_delete="CASCADE")

    class Meta:
        database = database

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)


BlocksToPages = Page.blocks.get_through_model()
