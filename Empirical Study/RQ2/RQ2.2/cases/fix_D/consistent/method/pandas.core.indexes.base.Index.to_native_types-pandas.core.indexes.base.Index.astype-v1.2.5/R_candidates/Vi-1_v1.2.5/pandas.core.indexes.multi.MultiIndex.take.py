    @Appender(_index_shared_docs["take"] % _index_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True, fill_value=None, **kwargs):
        nv.validate_take((), kwargs)
        indices = ensure_platform_int(indices)

        # only fill if we are passing a non-None fill_value
        allow_fill = self._maybe_disallow_fill(allow_fill, fill_value, indices)

        na_value = -1

        if allow_fill:
            taken = [lab.take(indices) for lab in self.codes]
            mask = indices == -1
            if mask.any():
                masked = []
                for new_label in taken:
                    label_values = new_label
                    label_values[mask] = na_value
                    masked.append(np.asarray(label_values))
                taken = masked
        else:
            taken = [lab.take(indices) for lab in self.codes]

        return MultiIndex(
            levels=self.levels, codes=taken, names=self.names, verify_integrity=False
        )
