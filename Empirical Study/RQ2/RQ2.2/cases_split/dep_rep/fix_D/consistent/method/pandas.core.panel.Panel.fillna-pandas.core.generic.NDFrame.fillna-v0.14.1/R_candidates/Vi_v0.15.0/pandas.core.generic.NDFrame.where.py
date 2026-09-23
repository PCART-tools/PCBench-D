    def where(self, cond, other=np.nan, inplace=False, axis=None, level=None,
              try_cast=False, raise_on_error=True):
        """
        Return an object of same shape as self and whose corresponding
        entries are from self where cond is True and otherwise are from other.

        Parameters
        ----------
        cond : boolean NDFrame or array
        other : scalar or NDFrame
        inplace : boolean, default False
            Whether to perform the operation in place on the data
        axis : alignment axis if needed, default None
        level : alignment level if needed, default None
        try_cast : boolean, default False
            try to cast the result back to the input type (if possible),
        raise_on_error : boolean, default True
            Whether to raise on invalid data types (e.g. trying to where on
            strings)

        Returns
        -------
        wh : same type as caller
        """
        if isinstance(cond, NDFrame):
            cond = cond.reindex(**self._construct_axes_dict())
        else:
            if not hasattr(cond, 'shape'):
                raise ValueError('where requires an ndarray like object for '
                                 'its condition')
            if cond.shape != self.shape:
                raise ValueError(
                    'Array conditional must be same shape as self')
            cond = self._constructor(cond, **self._construct_axes_dict())

        if inplace:
            cond = -(cond.fillna(True).astype(bool))
        else:
            cond = cond.fillna(False).astype(bool)

        # try to align
        try_quick = True
        if hasattr(other, 'align'):

            # align with me
            if other.ndim <= self.ndim:

                _, other = self.align(other, join='left',
                                      axis=axis, level=level,
                                      fill_value=np.nan)

                # if we are NOT aligned, raise as we cannot where index
                if (axis is None and
                        not all([other._get_axis(i).equals(ax)
                                 for i, ax in enumerate(self.axes)])):
                    raise InvalidIndexError

            # slice me out of the other
            else:
                raise NotImplemented(
                    "cannot align with a higher dimensional NDFrame"
                )

        elif is_list_like(other):

            if self.ndim == 1:

                # try to set the same dtype as ourselves
                new_other = np.array(other, dtype=self.dtype)
                if not (new_other == np.array(other)).all():
                    other = np.array(other)

                    # we can't use our existing dtype
                    # because of incompatibilities
                    try_quick = False
                else:
                    other = new_other
            else:

                other = np.array(other)

        if isinstance(other, np.ndarray):

            if other.shape != self.shape:

                if self.ndim == 1:

                    icond = cond.values

                    # GH 2745 / GH 4192
                    # treat like a scalar
                    if len(other) == 1:
                        other = np.array(other[0])

                    # GH 3235
                    # match True cond to other
                    elif len(cond[icond]) == len(other):

                        # try to not change dtype at first (if try_quick)
                        if try_quick:

                            try:
                                new_other = _values_from_object(self).copy()
                                new_other[icond] = other
                                other = new_other
                            except:
                                try_quick = False

                        # let's create a new (if we failed at the above
                        # or not try_quick
                        if not try_quick:

                            dtype, fill_value = _maybe_promote(other.dtype)
                            new_other = np.empty(len(icond), dtype=dtype)
                            new_other.fill(fill_value)
                            com._maybe_upcast_putmask(new_other, icond, other)
                            other = new_other

                    else:
                        raise ValueError(
                            'Length of replacements must equal series length')

                else:
                    raise ValueError('other must be the same shape as self '
                                     'when an ndarray')

            # we are the same shape, so create an actual object for alignment
            else:
                other = self._constructor(other, **self._construct_axes_dict())

        if inplace:
            # we may have different type blocks come out of putmask, so
            # reconstruct the block manager

            self._check_inplace_setting(other)
            new_data = self._data.putmask(mask=cond, new=other, align=axis is None,
                                          inplace=True)
            self._update_inplace(new_data)

        else:
            new_data = self._data.where(other=other, cond=cond, align=axis is None,
                                        raise_on_error=raise_on_error,
                                        try_cast=try_cast)

            return self._constructor(new_data).__finalize__(self)
