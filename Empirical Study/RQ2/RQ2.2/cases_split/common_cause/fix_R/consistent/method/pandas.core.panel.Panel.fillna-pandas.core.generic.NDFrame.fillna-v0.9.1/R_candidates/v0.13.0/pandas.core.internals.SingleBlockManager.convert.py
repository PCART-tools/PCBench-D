    def convert(self, *args, **kwargs):
        """ convert the whole block as one """
        kwargs['by_item'] = False
        return self.apply('convert', *args, **kwargs)
