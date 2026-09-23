    def _convert_slice_indexer(self, key: slice, kind: str, is_frame: bool = False):
        if not (key.step is None or key.step == 1):
            # GH#31658 if label-based, we require step == 1,
            #  if positional, we disallow float start/stop
            msg = "label-based slicing with step!=1 is not supported for IntervalIndex"
            if kind == "loc":
                raise ValueError(msg)
            elif kind == "getitem":
                if not is_valid_positional_slice(key):
                    # i.e. this cannot be interpreted as a positional slice
                    raise ValueError(msg)

        return super()._convert_slice_indexer(key, kind, is_frame=is_frame)
