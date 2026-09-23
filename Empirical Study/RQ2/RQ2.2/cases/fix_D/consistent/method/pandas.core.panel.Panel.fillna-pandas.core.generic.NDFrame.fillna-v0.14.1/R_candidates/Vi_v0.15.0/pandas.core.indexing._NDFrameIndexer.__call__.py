    def __call__(self, *args, **kwargs):
        # we need to return a copy of ourselves
        self = self.__class__(self.obj, self.name)

        # set the passed in values
        for k, v in compat.iteritems(kwargs):
            setattr(self,k,v)
        return self
