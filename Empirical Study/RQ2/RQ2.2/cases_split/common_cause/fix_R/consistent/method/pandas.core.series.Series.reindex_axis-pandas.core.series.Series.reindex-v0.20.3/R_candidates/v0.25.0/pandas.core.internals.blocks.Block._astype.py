    def _astype(self, dtype, copy=False, errors="raise", values=None, **kwargs):
        """Coerce to the new type

        Parameters
        ----------
        dtype : str, dtype convertible
        copy : boolean, default False
            copy if indicated
        errors : str, {'raise', 'ignore'}, default 'ignore'
            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object

        Returns
        -------
        Block
        """
        errors_legal_values = ("raise", "ignore")

        if errors not in errors_legal_values:
            invalid_arg = (
                "Expected value of kwarg 'errors' to be one of {}. "
                "Supplied value is '{}'".format(list(errors_legal_values), errors)
            )
            raise ValueError(invalid_arg)

        if inspect.isclass(dtype) and issubclass(dtype, ExtensionDtype):
            msg = (
                "Expected an instance of {}, but got the class instead. "
                "Try instantiating 'dtype'.".format(dtype.__name__)
            )
            raise TypeError(msg)

        # may need to convert to categorical
        if self.is_categorical_astype(dtype):

            # deprecated 17636
            for deprecated_arg in ("categories", "ordered"):
                if deprecated_arg in kwargs:
                    raise ValueError(
                        "Got an unexpected argument: {}".format(deprecated_arg)
                    )

            categories = kwargs.get("categories", None)
            ordered = kwargs.get("ordered", None)
            if com._any_not_none(categories, ordered):
                dtype = CategoricalDtype(categories, ordered)

            if is_categorical_dtype(self.values):
                # GH 10696/18593: update an existing categorical efficiently
                return self.make_block(self.values.astype(dtype, copy=copy))

            return self.make_block(Categorical(self.values, dtype=dtype))

        dtype = pandas_dtype(dtype)

        # astype processing
        if is_dtype_equal(self.dtype, dtype):
            if copy:
                return self.copy()
            return self

        if values is None:
            try:
                # force the copy here
                if self.is_extension:
                    values = self.values.astype(dtype)
                else:
                    if issubclass(dtype.type, str):

                        # use native type formatting for datetime/tz/timedelta
                        if self.is_datelike:
                            values = self.to_native_types()

                        # astype formatting
                        else:
                            values = self.get_values()

                    else:
                        values = self.get_values(dtype=dtype)

                    # _astype_nansafe works fine with 1-d only
                    vals1d = values.ravel()
                    values = astype_nansafe(vals1d, dtype, copy=True, **kwargs)

                # TODO(extension)
                # should we make this attribute?
                if isinstance(values, np.ndarray):
                    values = values.reshape(self.shape)

            except Exception:  # noqa: E722
                if errors == "raise":
                    raise
                newb = self.copy() if copy else self
            else:
                newb = make_block(values, placement=self.mgr_locs, ndim=self.ndim)
        else:
            newb = make_block(values, placement=self.mgr_locs, ndim=self.ndim)

        if newb.is_numeric and self.is_numeric:
            if newb.shape != self.shape:
                raise TypeError(
                    "cannot set astype for copy = [{copy}] for dtype "
                    "({dtype} [{shape}]) to different shape "
                    "({newb_dtype} [{newb_shape}])".format(
                        copy=copy,
                        dtype=self.dtype.name,
                        shape=self.shape,
                        newb_dtype=newb.dtype.name,
                        newb_shape=newb.shape,
                    )
                )
        return newb
