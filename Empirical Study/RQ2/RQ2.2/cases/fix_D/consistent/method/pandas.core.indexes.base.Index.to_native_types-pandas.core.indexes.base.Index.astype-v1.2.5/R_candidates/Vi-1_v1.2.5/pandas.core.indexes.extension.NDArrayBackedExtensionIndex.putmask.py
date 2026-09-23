    def putmask(self, mask, value):
        res_values = self._data.copy()
        try:
            res_values.putmask(mask, value)
        except (TypeError, ValueError):
            return self.astype(object).putmask(mask, value)

        return type(self)._simple_new(res_values, name=self.name)
