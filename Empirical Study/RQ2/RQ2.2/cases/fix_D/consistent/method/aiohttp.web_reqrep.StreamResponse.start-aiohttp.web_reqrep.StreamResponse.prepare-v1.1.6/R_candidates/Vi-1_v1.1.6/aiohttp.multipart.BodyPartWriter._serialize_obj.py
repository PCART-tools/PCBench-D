    def _serialize_obj(self):
        obj = self.obj
        mtype, stype, *_ = parse_mimetype(self.headers.get(CONTENT_TYPE))
        serializer = self._serialize_map.get((mtype, stype))
        if serializer is not None:
            return serializer(obj)

        for key in self._serialize_map:
            if not isinstance(key, tuple) and isinstance(obj, key):
                return self._serialize_map[key](obj)
        return self._serialize_default(obj)
