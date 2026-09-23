    def register(self, name):
        """
        Decorator for registering a class under a name.

        Example use::

            @registry.register(name)
            class Foo:
                pass
        """
        def wrapper(writer_cls):
            self._registered[name] = writer_cls
            return writer_cls
        return wrapper
