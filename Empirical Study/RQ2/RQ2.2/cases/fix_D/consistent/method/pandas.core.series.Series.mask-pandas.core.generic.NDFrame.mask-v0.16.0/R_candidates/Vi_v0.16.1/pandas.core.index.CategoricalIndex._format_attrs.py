    def _format_attrs(self):
        """
        Return a list of tuples of the (attr,formatted_value)
        """
        max_categories = (10 if get_option("display.max_categories") == 0
                    else get_option("display.max_categories"))
        attrs = [('categories', default_pprint(self.categories, max_seq_items=max_categories)),
                 ('ordered',self.ordered)]
        if self.name is not None:
            attrs.append(('name',default_pprint(self.name)))
        attrs.append(('dtype',"'%s'" % self.dtype))
        max_seq_items = get_option('display.max_seq_items')
        if len(self) > max_seq_items:
            attrs.append(('length',len(self)))
        return attrs
