    def get(self, data, *args, **kwargs):
        if isinstance(data, Payload):
            return data
        for factory, type in self._registry:
            if isinstance(data, type):
                return factory(data, *args, **kwargs)

        raise LookupError()
