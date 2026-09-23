    def __repr__(self):
        encoding = get_option('display.encoding')
        attrs = [('levels', default_pprint(self.levels)),
                 ('labels', default_pprint(self.labels))]
        if not all(name is None for name in self.names):
            attrs.append(('names', default_pprint(self.names)))
        if self.sortorder is not None:
            attrs.append(('sortorder', default_pprint(self.sortorder)))

        space = ' ' * (len(self.__class__.__name__) + 1)
        prepr = (u(",\n%s") % space).join([u("%s=%s") % (k, v)
                                          for k, v in attrs])
        res = u("%s(%s)") % (self.__class__.__name__, prepr)

        if not compat.PY3:
            # needs to be str in Python 2
            res = res.encode(encoding)
        return res
