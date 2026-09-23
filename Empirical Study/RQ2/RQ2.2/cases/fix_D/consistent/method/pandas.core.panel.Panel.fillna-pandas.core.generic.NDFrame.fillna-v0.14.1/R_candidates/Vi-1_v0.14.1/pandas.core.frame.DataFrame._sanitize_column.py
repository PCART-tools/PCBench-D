    def _sanitize_column(self, key, value):
        # Need to make sure new columns (which go into the BlockManager as new
        # blocks) are always copied

        if isinstance(value, (Series, DataFrame)):
            is_frame = isinstance(value, DataFrame)
            if value.index.equals(self.index) or not len(self.index):
                # copy the values
                value = value.values.copy()
            else:

                # GH 4107
                try:
                    value = value.reindex(self.index).values
                except Exception as e:

                    # duplicate axis
                    if not value.index.is_unique:
                        raise e

                    # other
                    raise TypeError('incompatible index of inserted column '
                                    'with frame index')

            if is_frame:
                value = value.T
        elif isinstance(value, Index) or _is_sequence(value):
            if len(value) != len(self.index):
                raise ValueError('Length of values does not match length of '
                                 'index')

            if not isinstance(value, (np.ndarray, Index)):
                if isinstance(value, list) and len(value) > 0:
                    value = com._possibly_convert_platform(value)
                else:
                    value = com._asarray_tuplesafe(value)
            elif isinstance(value, PeriodIndex):
                value = value.asobject
            elif isinstance(value, DatetimeIndex):
                value = value._to_embed(keep_tz=True).copy()
            elif value.ndim == 2:
                value = value.copy().T
            else:
                value = value.copy()
        else:
            # upcast the scalar
            dtype, value = _infer_dtype_from_scalar(value)
            value = np.repeat(value, len(self.index)).astype(dtype)
            value = com._possibly_cast_to_datetime(value, dtype)

        # broadcast across multiple columns if necessary
        if key in self.columns and value.ndim == 1:
            if not self.columns.is_unique or isinstance(self.columns,
                                                        MultiIndex):
                existing_piece = self[key]
                if isinstance(existing_piece, DataFrame):
                    value = np.tile(value, (len(existing_piece.columns), 1))

        return np.atleast_2d(np.asarray(value))
