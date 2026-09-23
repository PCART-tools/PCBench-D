    def __getstate__(self):
        meta = dict((k, getattr(self, k, None)) for k in self._metadata)
        return dict(_data=self._data, _typ=self._typ, _metadata=self._metadata,
                    **meta)
