    def _set_list(self, length, items):
        ptr = self._create_point(length, items)
        if ptr:
            capi.destroy_geom(self.ptr)
            self._ptr = ptr
            self._post_init()
        else:
            # can this happen?
            raise GEOSException('Geometry resulting from slice deletion was invalid.')
