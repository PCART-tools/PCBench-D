    @final
    def _where(
        self,
        cond,
        other=lib.no_default,
        inplace=False,
        axis=None,
        level=None,
        errors="raise",
    ):
        """
        Equivalent to public method `where`, except that `other` is not
        applied as a function even if callable. Used in __setitem__.
        """
        inplace = validate_bool_kwarg(inplace, "inplace")

        if axis is not None:
            axis = self._get_axis_number(axis)

        # align the cond to same shape as myself
        cond = com.apply_if_callable(cond, self)
        if isinstance(cond, NDFrame):
            cond, _ = cond.align(self, join="right", broadcast_axis=1, copy=False)
        else:
            if not hasattr(cond, "shape"):
                cond = np.asanyarray(cond)
            if cond.shape != self.shape:
                raise ValueError("Array conditional must be same shape as self")
            cond = self._constructor(cond, **self._construct_axes_dict())

        # make sure we are boolean
        fill_value = bool(inplace)
        cond = cond.fillna(fill_value)

        msg = "Boolean array expected for the condition, not {dtype}"

        if not cond.empty:
            if not isinstance(cond, ABCDataFrame):
                # This is a single-dimensional object.
                if not is_bool_dtype(cond):
                    raise ValueError(msg.format(dtype=cond.dtype))
            else:
                for dt in cond.dtypes:
                    if not is_bool_dtype(dt):
                        raise ValueError(msg.format(dtype=dt))
        else:
            # GH#21947 we have an empty DataFrame/Series, could be object-dtype
            cond = cond.astype(bool)

        cond = -cond if inplace else cond
        cond = cond.reindex(self._info_axis, axis=self._info_axis_number, copy=False)

        # try to align with other
        if isinstance(other, NDFrame):

            # align with me
            if other.ndim <= self.ndim:

                _, other = self.align(
                    other,
                    join="left",
                    axis=axis,
                    level=level,
                    fill_value=None,
                    copy=False,
                )

                # if we are NOT aligned, raise as we cannot where index
                if axis is None and not other._indexed_same(self):
                    raise InvalidIndexError

                elif other.ndim < self.ndim:
                    # TODO(EA2D): avoid object-dtype cast in EA case GH#38729
                    other = other._values
                    if axis == 0:
                        other = np.reshape(other, (-1, 1))
                    elif axis == 1:
                        other = np.reshape(other, (1, -1))

                    other = np.broadcast_to(other, self.shape)

            # slice me out of the other
            else:
                raise NotImplementedError(
                    "cannot align with a higher dimensional NDFrame"
                )

        elif not isinstance(other, (MultiIndex, NDFrame)):
            # mainly just catching Index here
            other = extract_array(other, extract_numpy=True)

        if isinstance(other, (np.ndarray, ExtensionArray)):

            if other.shape != self.shape:
                if self.ndim != 1:
                    # In the ndim == 1 case we may have
                    #  other length 1, which we treat as scalar (GH#2745, GH#4192)
                    #  or len(other) == icond.sum(), which we treat like
                    #  __setitem__ (GH#3235)
                    raise ValueError(
                        "other must be the same shape as self when an ndarray"
                    )

            # we are the same shape, so create an actual object for alignment
            else:
                other = self._constructor(other, **self._construct_axes_dict())

        if axis is None:
            axis = 0

        if self.ndim == getattr(other, "ndim", 0):
            align = True
        else:
            align = self._get_axis_number(axis) == 1

        if inplace:
            # we may have different type blocks come out of putmask, so
            # reconstruct the block manager

            self._check_inplace_setting(other)
            new_data = self._mgr.putmask(mask=cond, new=other, align=align)
            result = self._constructor(new_data)
            return self._update_inplace(result)

        else:
            new_data = self._mgr.where(
                other=other,
                cond=cond,
                align=align,
            )
            result = self._constructor(new_data)
            return result.__finalize__(self)
