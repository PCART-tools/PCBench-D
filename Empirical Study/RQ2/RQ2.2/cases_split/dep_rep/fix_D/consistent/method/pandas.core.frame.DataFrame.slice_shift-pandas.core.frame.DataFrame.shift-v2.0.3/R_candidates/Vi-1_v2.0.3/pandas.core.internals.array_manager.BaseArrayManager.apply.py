    def apply(
        self: T,
        f,
        align_keys: list[str] | None = None,
        **kwargs,
    ) -> T:
        """
        Iterate over the arrays, collect and create a new ArrayManager.

        Parameters
        ----------
        f : str or callable
            Name of the Array method to apply.
        align_keys: List[str] or None, default None
        **kwargs
            Keywords to pass to `f`

        Returns
        -------
        ArrayManager
        """
        assert "filter" not in kwargs

        align_keys = align_keys or []
        result_arrays: list[np.ndarray] = []
        # fillna: Series/DataFrame is responsible for making sure value is aligned

        aligned_args = {k: kwargs[k] for k in align_keys}

        if f == "apply":
            f = kwargs.pop("func")

        for i, arr in enumerate(self.arrays):
            if aligned_args:
                for k, obj in aligned_args.items():
                    if isinstance(obj, (ABCSeries, ABCDataFrame)):
                        # The caller is responsible for ensuring that
                        #  obj.axes[-1].equals(self.items)
                        if obj.ndim == 1:
                            kwargs[k] = obj.iloc[i]
                        else:
                            kwargs[k] = obj.iloc[:, i]._values
                    else:
                        # otherwise we have an array-like
                        kwargs[k] = obj[i]

            if callable(f):
                applied = f(arr, **kwargs)
            else:
                applied = getattr(arr, f)(**kwargs)

            # if not isinstance(applied, ExtensionArray):
            #     # TODO not all EA operations return new EAs (eg astype)
            #     applied = array(applied)
            result_arrays.append(applied)

        new_axes = self._axes

        # error: Argument 1 to "ArrayManager" has incompatible type "List[ndarray]";
        # expected "List[Union[ndarray, ExtensionArray]]"
        return type(self)(result_arrays, new_axes)  # type: ignore[arg-type]
