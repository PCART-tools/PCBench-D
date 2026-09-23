    @cache_readonly
    def str(self):
        from pandas.core.strings import StringMethods
        return StringMethods(self)
