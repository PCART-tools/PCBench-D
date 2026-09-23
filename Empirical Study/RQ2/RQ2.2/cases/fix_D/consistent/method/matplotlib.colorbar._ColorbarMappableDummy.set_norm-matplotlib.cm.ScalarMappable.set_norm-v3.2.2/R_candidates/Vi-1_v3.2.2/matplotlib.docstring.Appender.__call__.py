    def __call__(self, func):
        docitems = [func.__doc__, self.addendum]
        func.__doc__ = func.__doc__ and self.join.join(docitems)
        return func
