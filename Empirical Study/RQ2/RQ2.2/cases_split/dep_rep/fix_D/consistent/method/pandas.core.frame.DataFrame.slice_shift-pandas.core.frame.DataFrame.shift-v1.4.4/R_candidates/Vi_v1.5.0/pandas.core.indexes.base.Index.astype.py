    def astype(self, dtype, copy: bool = True):
        """
        Create an Index with values cast to dtypes.

        The class of a new Index is determined by dtype. When conversion is
        impossible, a TypeError exception is raised.

        Parameters
        ----------
        dtype : numpy dtype or pandas type
            Note that any signed integer `dtype` is treated as ``'int64'``,
            and any unsigned integer `dtype` is treated as ``'uint64'``,
            regardless of the size.
        copy : bool, default True
            By default, astype always returns a newly allocated object.
            If copy is set to False and internal requirements on dtype are
            satisfied, the original data is used to create a new Index
            or the original Index is returned.

        Returns
        -------
        Index
            Index with values cast to specified dtype.
        """
        if dtype is not None:
            dtype = pandas_dtype(dtype)

        if is_dtype_equal(self.dtype, dtype):
            # Ensure that self.astype(self.dtype) is self
            return self.copy() if copy else self

        values = self._data
        if isinstance(values, ExtensionArray):
            if isinstance(dtype, np.dtype) and dtype.kind == "M" and is_unitless(dtype):
                # TODO(2.0): remove this special-casing once this is enforced
                #  in DTA.astype
                raise TypeError(f"Cannot cast {type(self).__name__} to dtype")

            with rewrite_exception(type(values).__name__, type(self).__name__):
                new_values = values.astype(dtype, copy=copy)

        elif is_float_dtype(self.dtype) and needs_i8_conversion(dtype):
            # NB: this must come before the ExtensionDtype check below
            # TODO: this differs from Series behavior; can/should we align them?
            raise TypeError(
                f"Cannot convert Float64Index to dtype {dtype}; integer "
                "values are required for conversion"
            )

        elif isinstance(dtype, ExtensionDtype):
            cls = dtype.construct_array_type()
            # Note: for RangeIndex and CategoricalDtype self vs self._values
            #  behaves differently here.
            new_values = cls._from_sequence(self, dtype=dtype, copy=copy)

        else:
            try:
                if dtype == str:
                    # GH#38607
                    new_values = values.astype(dtype, copy=copy)
                else:
                    # GH#13149 specifically use astype_nansafe instead of astype
                    new_values = astype_nansafe(values, dtype=dtype, copy=copy)
            except IntCastingNaNError:
                raise
            except (TypeError, ValueError) as err:
                if dtype.kind == "u" and "losslessly" in str(err):
                    # keep the message from _astype_float_to_int_nansafe
                    raise
                raise TypeError(
                    f"Cannot cast {type(self).__name__} to dtype {dtype}"
                ) from err

        # pass copy=False because any copying will be done in the astype above
        if self._is_backward_compat_public_numeric_index:
            # this block is needed so e.g. NumericIndex[int8].astype("int32") returns
            # NumericIndex[int32] and not Int64Index with dtype int64.
            # When Int64Index etc. are removed from the code base, removed this also.
            if isinstance(dtype, np.dtype) and is_numeric_dtype(dtype):
                return self._constructor(
                    new_values, name=self.name, dtype=dtype, copy=False
                )
        return Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
