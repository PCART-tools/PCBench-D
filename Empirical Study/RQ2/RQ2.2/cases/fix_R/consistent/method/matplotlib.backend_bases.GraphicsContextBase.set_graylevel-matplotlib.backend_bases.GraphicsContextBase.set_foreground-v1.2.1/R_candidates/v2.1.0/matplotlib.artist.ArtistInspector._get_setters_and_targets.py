    def _get_setters_and_targets(self):
        """
        Get the attribute strings and a full path to where the setter
        is defined for all setters in an object.
        """

        setters = []
        for name in dir(self.o):
            if not name.startswith('set_'):
                continue
            func = getattr(self.o, name)
            if not callable(func):
                continue
            if six.PY2:
                nargs = len(inspect.getargspec(func)[0])
            else:
                nargs = len(inspect.getfullargspec(func)[0])
            if nargs < 2 or self.is_alias(func):
                continue
            source_class = self.o.__module__ + "." + self.o.__name__
            for cls in self.o.mro():
                if name in cls.__dict__:
                    source_class = cls.__module__ + "." + cls.__name__
                    break
            setters.append((name[4:], source_class + "." + name))
        return setters
