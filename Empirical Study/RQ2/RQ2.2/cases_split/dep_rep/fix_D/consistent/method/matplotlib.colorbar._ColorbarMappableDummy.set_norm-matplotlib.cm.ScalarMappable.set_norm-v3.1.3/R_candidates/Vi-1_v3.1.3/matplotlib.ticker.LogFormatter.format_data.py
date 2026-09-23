    def format_data(self, value):
        b = self.labelOnlyBase
        self.labelOnlyBase = False
        value = cbook.strip_math(self.__call__(value))
        self.labelOnlyBase = b
        return value
