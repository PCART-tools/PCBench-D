    def isna(self, func, **kwargs):
        return self.apply("apply", func=func, **kwargs)
