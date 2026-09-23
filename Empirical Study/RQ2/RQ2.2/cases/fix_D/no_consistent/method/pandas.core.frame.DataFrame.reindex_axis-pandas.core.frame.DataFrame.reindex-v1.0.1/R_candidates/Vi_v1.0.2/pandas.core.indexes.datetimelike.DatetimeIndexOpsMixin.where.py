    @Appender(_index_shared_docs["where"] % _index_doc_kwargs)
    def where(self, cond, other=None):
        values = self.view("i8")

        if is_scalar(other) and isna(other):
            other = NaT.value

        else:
            # Do type inference if necessary up front
            # e.g. we passed PeriodIndex.values and got an ndarray of Periods
            other = Index(other)

            if is_categorical_dtype(other):
                # e.g. we have a Categorical holding self.dtype
                if needs_i8_conversion(other.categories):
                    other = other._internal_get_values()

            if not is_dtype_equal(self.dtype, other.dtype):
                raise TypeError(f"Where requires matching dtype, not {other.dtype}")

            other = other.view("i8")

        result = np.where(cond, values, other).astype("i8")
        return self._shallow_copy(result)
