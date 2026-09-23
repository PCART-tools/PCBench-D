    def convert_value(self, v) -> "TermValue":
        """ convert the expression that is in the term to something that is
        accepted by pytables """

        def stringify(value):
            if self.encoding is not None:
                encoder = partial(pprint_thing_encoded, encoding=self.encoding)
            else:
                encoder = pprint_thing
            return encoder(value)

        kind = _ensure_decoded(self.kind)
        meta = _ensure_decoded(self.meta)
        if kind == "datetime64" or kind == "datetime":
            if isinstance(v, (int, float)):
                v = stringify(v)
            v = _ensure_decoded(v)
            v = Timestamp(v)
            if v.tz is not None:
                v = v.tz_convert("UTC")
            return TermValue(v, v.value, kind)
        elif kind == "timedelta64" or kind == "timedelta":
            v = Timedelta(v, unit="s").value
            return TermValue(int(v), v, kind)
        elif meta == "category":
            metadata = com.values_from_object(self.metadata)
            result = metadata.searchsorted(v, side="left")

            # result returns 0 if v is first element or if v is not in metadata
            # check that metadata contains v
            if not result and v not in metadata:
                result = -1
            return TermValue(result, result, "integer")
        elif kind == "integer":
            v = int(float(v))
            return TermValue(v, v, kind)
        elif kind == "float":
            v = float(v)
            return TermValue(v, v, kind)
        elif kind == "bool":
            if isinstance(v, str):
                v = not v.strip().lower() in [
                    "false",
                    "f",
                    "no",
                    "n",
                    "none",
                    "0",
                    "[]",
                    "{}",
                    "",
                ]
            else:
                v = bool(v)
            return TermValue(v, v, kind)
        elif isinstance(v, str):
            # string quoting
            return TermValue(v, stringify(v), "string")
        else:
            raise TypeError(f"Cannot compare {v} of type {type(v)} to {kind} column")
