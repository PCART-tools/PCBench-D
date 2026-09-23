    def get_setters(self):
        """
        Get the attribute strings with setters for object.

        For example, for a line, return ``['markerfacecolor', 'linewidth',
        ....]``.
        """
        setters = []
        for name in dir(self.o):
            if not name.startswith('set_'):
                continue
            func = getattr(self.o, name)
            if (not callable(func)
                    or self.number_of_parameters(func) < 2
                    or self.is_alias(func)):
                continue
            setters.append(name[4:])
        return setters
