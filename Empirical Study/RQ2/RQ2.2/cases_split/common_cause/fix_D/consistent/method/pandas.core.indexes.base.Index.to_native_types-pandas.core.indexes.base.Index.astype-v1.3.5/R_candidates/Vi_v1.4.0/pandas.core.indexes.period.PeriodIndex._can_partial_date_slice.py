    def _can_partial_date_slice(self, reso: Resolution) -> bool:
        assert isinstance(reso, Resolution), (type(reso), reso)
        # e.g. test_getitem_setitem_periodindex
        return reso > self.dtype.resolution
