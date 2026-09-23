    def to_string(self, pretty=False):
        divider = '\n  ' if pretty else ' '
        return '{}{}{}'.format(
            self.__class__.__name__,
            divider,
            divider.join('{}={}'.format(k, truncate(v)) for k, v in self.__values__.items()),
        )
