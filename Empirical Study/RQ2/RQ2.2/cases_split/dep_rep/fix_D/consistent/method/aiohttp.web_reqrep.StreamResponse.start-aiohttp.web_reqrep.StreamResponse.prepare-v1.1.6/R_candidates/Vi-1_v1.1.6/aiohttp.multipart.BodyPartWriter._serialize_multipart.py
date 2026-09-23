    def _serialize_multipart(self, obj):
        yield from obj.serialize()
