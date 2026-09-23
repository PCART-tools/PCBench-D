    def _get_concat_axis(self) -> Index:
        """
        Return index to be used along concatenation axis.
        """
        if self._is_series:
            if self.axis == 0:
                indexes = [x.index for x in self.objs]
            elif self.ignore_index:
                idx = ibase.default_index(len(self.objs))
                return idx
            elif self.keys is None:
                names: List[Optional[Hashable]] = [None] * len(self.objs)
                num = 0
                has_names = False
                for i, x in enumerate(self.objs):
                    if not isinstance(x, Series):
                        raise TypeError(
                            f"Cannot concatenate type 'Series' with "
                            f"object of type '{type(x).__name__}'"
                        )
                    if x.name is not None:
                        names[i] = x.name
                        has_names = True
                    else:
                        names[i] = num
                        num += 1
                if has_names:
                    return Index(names)
                else:
                    return ibase.default_index(len(self.objs))
            else:
                return ensure_index(self.keys).set_names(self.names)
        else:
            indexes = [x._data.axes[self.axis] for x in self.objs]

        if self.ignore_index:
            idx = ibase.default_index(sum(len(i) for i in indexes))
            return idx

        if self.keys is None:
            concat_axis = _concat_indexes(indexes)
        else:
            concat_axis = _make_concat_multiindex(
                indexes, self.keys, self.levels, self.names
            )

        self._maybe_check_integrity(concat_axis)

        return concat_axis
