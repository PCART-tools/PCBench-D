    def __getstate__(self):
        # pickling
        return dict(_typ=self._typ, _subtyp=self._subtyp, _data=self._data,
                    _default_fill_value=self._default_fill_value,
                    _default_kind=self._default_kind)
