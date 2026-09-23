    @doc(ExtensionArray.factorize)
    def factorize(
        self,
        na_sentinel: int | lib.NoDefault = lib.no_default,
        use_na_sentinel: bool | lib.NoDefault = lib.no_default,
    ) -> tuple[np.ndarray, ExtensionArray]:
        resolved_na_sentinel = resolve_na_sentinel(na_sentinel, use_na_sentinel)
        if pa_version_under4p0:
            encoded = self._data.dictionary_encode()
        else:
            null_encoding = "mask" if resolved_na_sentinel is not None else "encode"
            encoded = self._data.dictionary_encode(null_encoding=null_encoding)
        indices = pa.chunked_array(
            [c.indices for c in encoded.chunks], type=encoded.type.index_type
        ).to_pandas()
        if indices.dtype.kind == "f":
            indices[np.isnan(indices)] = (
                resolved_na_sentinel if resolved_na_sentinel is not None else -1
            )
        indices = indices.astype(np.int64, copy=False)

        if encoded.num_chunks:
            uniques = type(self)(encoded.chunk(0).dictionary)
            if resolved_na_sentinel is None and pa_version_under4p0:
                # TODO: share logic with BaseMaskedArray.factorize
                # Insert na with the proper code
                na_mask = indices.values == -1
                na_index = na_mask.argmax()
                if na_mask[na_index]:
                    uniques = uniques.insert(na_index, self.dtype.na_value)
                    na_code = 0 if na_index == 0 else indices[:na_index].argmax() + 1
                    indices[indices >= na_code] += 1
                    indices[indices == -1] = na_code
        else:
            uniques = type(self)(pa.array([], type=encoded.type.value_type))

        return indices.values, uniques
