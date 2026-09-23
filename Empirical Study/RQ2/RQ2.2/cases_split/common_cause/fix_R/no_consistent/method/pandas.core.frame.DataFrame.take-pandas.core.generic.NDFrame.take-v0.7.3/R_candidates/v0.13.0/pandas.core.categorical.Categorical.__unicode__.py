    def __unicode__(self):
        width, height = get_terminal_size()
        max_rows = (height if get_option("display.max_rows") == 0
                    else get_option("display.max_rows"))
        if len(self.labels) > (max_rows or 1000):
            result = self._tidy_repr(min(30, max_rows) - 4)
        elif len(self.labels) > 0:
            result = self._get_repr(length=len(self) > 50,
                                    name=True)
        else:
            result = 'Categorical([], %s' % self._get_repr(name=True,
                                                           length=False,
                                                           footer=True,
                                                           )

        return result
