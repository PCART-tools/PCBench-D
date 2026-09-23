    def __unicode__(self):
        # unicode representation based upon iterating over self
        # (since, by definition, `PandasContainers` are iterable)
        prepr = '[%s]' % ','.join(map(pprint_thing, self))
        return '%s(%s)' % (self.__class__.__name__, prepr)
