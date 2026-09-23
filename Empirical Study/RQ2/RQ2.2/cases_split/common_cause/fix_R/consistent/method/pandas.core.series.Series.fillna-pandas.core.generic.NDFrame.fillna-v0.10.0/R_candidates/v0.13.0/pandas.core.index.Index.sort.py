    def sort(self, *args, **kwargs):
        raise TypeError('Cannot sort an %r object' % self.__class__.__name__)
