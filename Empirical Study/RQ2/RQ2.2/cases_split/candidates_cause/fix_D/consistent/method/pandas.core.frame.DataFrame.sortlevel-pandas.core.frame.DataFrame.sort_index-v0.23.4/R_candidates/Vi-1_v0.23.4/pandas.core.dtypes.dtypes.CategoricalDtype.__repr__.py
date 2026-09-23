    def __repr__(self):
        tpl = u'CategoricalDtype(categories={}ordered={})'
        if self.categories is None:
            data = u"None, "
        else:
            data = self.categories._format_data(name=self.__class__.__name__)
        return tpl.format(data, self.ordered)
