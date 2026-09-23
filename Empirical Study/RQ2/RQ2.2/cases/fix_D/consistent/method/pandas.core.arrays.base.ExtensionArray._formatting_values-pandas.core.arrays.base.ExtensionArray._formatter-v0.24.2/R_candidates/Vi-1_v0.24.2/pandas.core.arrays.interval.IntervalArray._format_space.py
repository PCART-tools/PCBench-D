    def _format_space(self):
        space = ' ' * (len(self.__class__.__name__) + 1)
        return "\n{space}".format(space=space)
