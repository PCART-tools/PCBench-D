    def _is_dtype_compat(self, other):
        """
        *this is an internal non-public method*

        provide a comparison between the dtype of self and other (coercing if
        needed)

        Raises
        ------
        TypeError if the dtypes are not compatible
        """
        if is_categorical_dtype(other):
            if isinstance(other, CategoricalIndex):
                other = other._values
            if not other.is_dtype_equal(self):
                raise TypeError(
                    "categories must match existing categories " "when appending"
                )
        else:
            values = other
            if not is_list_like(values):
                values = [values]
            other = CategoricalIndex(self._create_categorical(other, dtype=self.dtype))
            if not other.isin(values).all():
                raise TypeError(
                    "cannot append a non-category item to a " "CategoricalIndex"
                )

        return other
