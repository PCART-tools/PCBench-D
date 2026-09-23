    def _sanitize_mixed_ndim(
        self,
        objs: list[Series | DataFrame],
        sample: Series | DataFrame,
        ignore_index: bool,
        axis: AxisInt,
    ) -> tuple[list[Series | DataFrame], Series | DataFrame]:
        # if we have mixed ndims, then convert to highest ndim
        # creating column numbers as needed

        new_objs = []

        current_column = 0
        max_ndim = sample.ndim
        for obj in objs:
            ndim = obj.ndim
            if ndim == max_ndim:
                pass

            elif ndim != max_ndim - 1:
                raise ValueError(
                    "cannot concatenate unaligned mixed dimensional NDFrame objects"
                )

            else:
                name = getattr(obj, "name", None)
                if ignore_index or name is None:
                    name = current_column
                    current_column += 1

                # doing a row-wise concatenation so need everything
                # to line up
                if self._is_frame and axis == 1:
                    name = 0

                obj = sample._constructor({name: obj}, copy=False)

            new_objs.append(obj)

        return new_objs, sample
