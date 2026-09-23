    @Appender(_index_shared_docs["take"] % _index_doc_kwargs)
    def take(
        self: MultiIndex,
        indices,
        axis: Axis = 0,
        allow_fill: bool = True,
        fill_value=None,
        **kwargs,
    ) -> MultiIndex:
        nv.validate_take((), kwargs)
        indices = ensure_platform_int(indices)

        # only fill if we are passing a non-None fill_value
        allow_fill = self._maybe_disallow_fill(allow_fill, fill_value, indices)

        na_value = -1

        taken = [lab.take(indices) for lab in self.codes]
        if allow_fill:
            mask = indices == -1
            if mask.any():
                masked = []
                for new_label in taken:
                    label_values = new_label
                    label_values[mask] = na_value
                    masked.append(np.asarray(label_values))
                taken = masked

        return MultiIndex(
            levels=self.levels, codes=taken, names=self.names, verify_integrity=False
        )
