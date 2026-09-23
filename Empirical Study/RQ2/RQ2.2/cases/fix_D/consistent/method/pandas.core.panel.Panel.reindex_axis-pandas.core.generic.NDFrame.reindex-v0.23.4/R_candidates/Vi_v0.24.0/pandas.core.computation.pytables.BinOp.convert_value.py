    def convert_value(self, v):
        """ convert the expression that is in the term to something that is
        accepted by pytables """

        def stringify(value):
            if self.encoding is not None:
                encoder = partial(pprint_thing_encoded,
                                  encoding=self.encoding)
            else:
                encoder = pprint_thing
            return encoder(value)

        kind = _ensure_decoded(self.kind)
        meta = _ensure_decoded(self.meta)
        if kind == u('datetime64') or kind == u('datetime'):
            if isinstance(v, (int, float)):
                v = stringify(v)
            v = _ensure_decoded(v)
            v = pd.Timestamp(v)
            if v.tz is not None:
                v = v.tz_convert('UTC')
            return TermValue(v, v.value, kind)
        elif kind == u('timedelta64') or kind == u('timedelta'):
            v = pd.Timedelta(v, unit='s').value
            return TermValue(int(v), v, kind)
        elif meta == u('category'):
            metadata = com.values_from_object(self.metadata)
            result = metadata.searchsorted(v, side='left')

            # result returns 0 if v is first element or if v is not in metadata
            # check that metadata contains v
            if not result and v not in metadata:
                result = -1
            return TermValue(result, result, u('integer'))
        elif kind == u('integer'):
            v = int(float(v))
            return TermValue(v, v, kind)
        elif kind == u('float'):
            v = float(v)
            return TermValue(v, v, kind)
        elif kind == u('bool'):
            if isinstance(v, string_types):
                v = not v.strip().lower() in [u('false'), u('f'), u('no'),
                                              u('n'), u('none'), u('0'),
                                              u('[]'), u('{}'), u('')]
            else:
                v = bool(v)
            return TermValue(v, v, kind)
        elif isinstance(v, string_types):
            # string quoting
            return TermValue(v, stringify(v), u('string'))
        else:
            raise TypeError("Cannot compare {v} of type {typ} to {kind} column"
                            .format(v=v, typ=type(v), kind=kind))
