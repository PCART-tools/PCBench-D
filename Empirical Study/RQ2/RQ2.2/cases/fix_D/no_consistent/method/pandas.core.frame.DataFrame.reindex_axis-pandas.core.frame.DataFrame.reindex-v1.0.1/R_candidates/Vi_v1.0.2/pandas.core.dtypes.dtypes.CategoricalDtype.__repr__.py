    def __repr__(self) -> str_type:
        tpl = "CategoricalDtype(categories={data}ordered={ordered})"
        if self.categories is None:
            data = "None, "
        else:
            data = self.categories._format_data(name=type(self).__name__)
        return tpl.format(data=data, ordered=self.ordered)
