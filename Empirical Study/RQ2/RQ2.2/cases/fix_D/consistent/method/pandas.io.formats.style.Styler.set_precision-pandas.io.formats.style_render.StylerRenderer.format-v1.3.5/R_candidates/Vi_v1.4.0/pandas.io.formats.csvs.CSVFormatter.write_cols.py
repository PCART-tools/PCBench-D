    @property
    def write_cols(self) -> Sequence[Hashable]:
        if self._has_aliases:
            assert not isinstance(self.header, bool)
            if len(self.header) != len(self.cols):
                raise ValueError(
                    f"Writing {len(self.cols)} cols but got {len(self.header)} aliases"
                )
            else:
                return self.header
        else:
            # self.cols is an ndarray derived from Index._format_native_types,
            #  so its entries are strings, i.e. hashable
            return cast(Sequence[Hashable], self.cols)
