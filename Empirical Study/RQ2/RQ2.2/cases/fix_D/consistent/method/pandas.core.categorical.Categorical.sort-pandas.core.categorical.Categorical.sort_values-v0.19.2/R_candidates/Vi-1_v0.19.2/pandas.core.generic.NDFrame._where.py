    def _where(self, cond, other=np.nan, inplace=False, axis=None, level=None,
               try_cast=False, raise_on_error=True):
        """
        Equivalent to public method `where`, except that `other` is not
        applied as a function even if callable. Used in __setitem__.
        """

        cond = com._apply_if_callable(cond, self)

        if isinstance(cond, NDFrame):
            cond, _ = cond.align(self, join='right', broadcast_axis=1)
        else:
            if not hasattr(cond, 'shape'):
                raise ValueError('where requires an ndarray like object for '
                                 'its condition')
            if cond.shape != self.shape:
                raise ValueError('Array conditional must be same shape as '
                                 'self')
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

                _, other = self.align(other, join='left', axis=axis,
                                      level=level, fill_value=np.nan)

                # if we are NOT aligned, raise as we cannot where index
                if (axis is None and
                        not all([other._get_axis(i).equals(ax)
                                 for i, ax in enumerate(self.axes)])):
                    raise InvalidIndexError

            # slice me out of the other
            else:
                raise NotImplemented("cannot align with a higher dimensional "
                                     "NDFrame")

        elif is_list_like(other):

            if self.ndim == 1:

                # try to set the same dtype as ourselves
                try:
                    new_other = np.array(other, dtype=self.dtype)
                except ValueError:
                    new_other = np.array(other)
                except TypeError:
                    new_other = other

                # we can end up comparing integers and m8[ns]
                # which is a numpy no no
                is_i8 = needs_i8_conversion(self.dtype)
                if is_i8:
                    matches = False
                else:
                    matches = (new_other == np.array(other))

                if matches is False or not matches.all():

                    # coerce other to a common dtype if we can
                    if needs_i8_conversion(self.dtype):
                        try:
                            other = np.array(other, dtype=self.dtype)
                        except:
                            other = np.array(other)
                    else:
                        other = np.asarray(other)
                        other = np.asarray(other,
                                           dtype=np.common_type(other,
                                                                new_other))

                    # we need to use the new dtype
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
                            _maybe_upcast_putmask(new_other, icond, other)
                            other = new_other

                    else:
                        raise ValueError('Length of replacements must equal '
                                         'series length')

                else:
                    raise ValueError('other must be the same shape as self '
                                     'when an ndarray')

            # we are the same shape, so create an actual object for alignment
            else:
                other = self._constructor(other, **self._construct_axes_dict())

        if axis is None:
            axis = 0

        if self.ndim == getattr(other, 'ndim', 0):
            align = True
        else:
            align = (self._get_axis_number(axis) == 1)

        block_axis = self._get_block_manager_axis(axis)

        if inplace:
            # we may have different type blocks come out of putmask, so
            # reconstruct the block manager

            self._check_inplace_setting(other)
            new_data = self._data.putmask(mask=cond, new=other, align=align,
                                          inplace=True, axis=block_axis,
                                          transpose=self._AXIS_REVERSED)
            self._update_inplace(new_data)

        else:
            new_data = self._data.where(other=other, cond=cond, align=align,
                                        raise_on_error=raise_on_error,
                                        try_cast=try_cast, axis=block_axis,
                                        transpose=self._AXIS_REVERSED)

            return self._constructor(new_data).__finalize__(self)
