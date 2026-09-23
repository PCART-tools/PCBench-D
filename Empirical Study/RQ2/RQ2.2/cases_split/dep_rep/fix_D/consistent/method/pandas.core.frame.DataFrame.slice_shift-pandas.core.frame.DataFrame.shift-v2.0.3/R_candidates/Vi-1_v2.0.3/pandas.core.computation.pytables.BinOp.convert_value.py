    def convert_value(self, v) -> TermValue:
        """
        convert the expression that is in the term to something that is
        accepted by pytables
        """

        def stringify(value):
            if self.encoding is not None:
                return pprint_thing_encoded(value, encoding=self.encoding)
            return pprint_thing(value)

        kind = ensure_decoded(self.kind)
        meta = ensure_decoded(self.meta)
        if kind in ("datetime64", "datetime"):
            if isinstance(v, (int, float)):
                v = stringify(v)
            v = ensure_decoded(v)
            v = Timestamp(v).as_unit("ns")
            if v.tz is not None:
                v = v.tz_convert("UTC")
            return TermValue(v, v._value, kind)
        elif kind in ("timedelta64", "timedelta"):
            if isinstance(v, str):
                v = Timedelta(v)
            else:
                v = Timedelta(v, unit="s")
            v = v.as_unit("ns")._value
            return TermValue(int(v), v, kind)
        elif meta == "category":
            metadata = extract_array(self.metadata, extract_numpy=True)
            result: npt.NDArray[np.intp] | np.intp | int
            if v not in metadata:
                result = -1
            else:
                result = metadata.searchsorted(v, side="left")
            return TermValue(result, result, "integer")
        elif kind == "integer":
            v = int(float(v))
            return TermValue(v, v, kind)
        elif kind == "float":
            v = float(v)
            return TermValue(v, v, kind)
        elif kind == "bool":
            if isinstance(v, str):
                v = v.strip().lower() not in [
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
