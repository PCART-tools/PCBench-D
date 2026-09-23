    def __repr__(self):
        d = dict(self.__dict__)
        del d['file']
        del d['parent']
        return repr(d)
