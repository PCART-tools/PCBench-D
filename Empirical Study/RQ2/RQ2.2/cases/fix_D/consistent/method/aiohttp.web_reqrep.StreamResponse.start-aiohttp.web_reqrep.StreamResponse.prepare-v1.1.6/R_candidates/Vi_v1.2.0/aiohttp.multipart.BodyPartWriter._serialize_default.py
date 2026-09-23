    def _serialize_default(self, obj):
        raise TypeError('unknown body part type %r' % type(obj))
