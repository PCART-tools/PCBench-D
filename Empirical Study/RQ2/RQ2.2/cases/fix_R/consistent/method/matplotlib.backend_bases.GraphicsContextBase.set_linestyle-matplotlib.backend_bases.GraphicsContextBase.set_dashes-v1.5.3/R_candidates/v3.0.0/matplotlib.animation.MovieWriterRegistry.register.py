    def register(self, name):
        """Decorator for registering a class under a name.

        Example use::

            @registry.register(name)
            class Foo:
                pass
        """
        def wrapper(writerClass):
            self._registered[name] = writerClass
            if writerClass.isAvailable():
                self.avail[name] = writerClass
            return writerClass
        return wrapper
