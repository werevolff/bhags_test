from marshmallow import Schema, fields


class BlockShortSchema(Schema):
    name = fields.Str()
    ordering = fields.Int()


class BlockDetailSchema(BlockShortSchema):
    video_url = fields.Str()
    views = fields.Int()
    increment_url = fields.Method("get_increment_url")

    def get_increment_url(self, instance):
        return str(
            self.context["request"]
            .app.router["block-viewed"]
            .url_for(id=str(instance.id))
        )


class PageListSchema(Schema):
    name = fields.Str()
    ordering = fields.Int()
    blocks = fields.Nested(BlockShortSchema, many=True)
    url = fields.Method("get_url")

    def get_url(self, instance):
        return str(
            self.context["request"]
            .app.router["pages-detail"]
            .url_for(slug=instance.slug)
        )


class PageDetailSchema(PageListSchema):
    blocks = fields.Nested(BlockDetailSchema, many=True)
