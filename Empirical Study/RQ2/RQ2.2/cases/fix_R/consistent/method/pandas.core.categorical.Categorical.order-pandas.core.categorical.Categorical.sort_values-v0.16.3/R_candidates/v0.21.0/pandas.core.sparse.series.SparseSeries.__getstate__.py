    def __getstate__(self):
        # pickling
        return dict(_typ=self._typ, _subtyp=self._subtyp, _data=self._data,
                    fill_value=self.fill_value, name=self.name)
