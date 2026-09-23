    def __getstate__(self):
        d = self.__dict__.copy()
        # turn the dictionary with weak values into a normal dictionary
        d['_parents'] = dict((k, v()) for (k, v) in
                             six.iteritems(self._parents))
        return d
