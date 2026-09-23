    def astype(self, dtype: AstypeArg, copy: bool = True) -> ArrayLike:
        """
        Coerce this type to another dtype

        Parameters
        ----------
        dtype : numpy dtype or pandas type
        copy : bool, default True
            By default, astype always returns a newly allocated object.
            If copy is set to False and dtype is categorical, the original
            object is returned.
        """
        dtype = pandas_dtype(dtype)
        if self.dtype is dtype:
            result = self.copy() if copy else self

        elif is_categorical_dtype(dtype):
            dtype = cast("Union[str, CategoricalDtype]", dtype)

            # GH 10696/18593/18630
            dtype = self.dtype.update_dtype(dtype)
            self = self.copy() if copy else self
            result = self._set_dtype(dtype)

        elif isinstance(dtype, ExtensionDtype):
            return super().astype(dtype, copy=copy)

        elif is_integer_dtype(dtype) and self.isna().any():
            raise ValueError("Cannot convert float NaN to integer")

        elif len(self.codes) == 0 or len(self.categories) == 0:
            result = np.array(
                self,
                dtype=dtype,
                copy=copy,
            )

        else:
            # GH8628 (PERF): astype category codes instead of astyping array
            new_cats = self.categories._values

            try:
                new_cats = new_cats.astype(dtype=dtype, copy=copy)
                fill_value = self.categories._na_value
                if not is_valid_na_for_dtype(fill_value, dtype):
                    fill_value = lib.item_from_zerodim(
                        np.array(self.categories._na_value).astype(dtype)
                    )
            except (
                TypeError,  # downstream error msg for CategoricalIndex is misleading
                ValueError,
            ):
                msg = f"Cannot cast {self.categories.dtype} dtype to {dtype}"
                raise ValueError(msg)

            result = take_nd(
                new_cats, ensure_platform_int(self._codes), fill_value=fill_value
            )

        return result
