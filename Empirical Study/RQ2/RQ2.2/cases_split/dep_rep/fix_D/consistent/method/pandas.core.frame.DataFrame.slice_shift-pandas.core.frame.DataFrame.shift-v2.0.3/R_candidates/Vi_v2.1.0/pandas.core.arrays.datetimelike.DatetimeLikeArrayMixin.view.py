    def view(self, dtype: Dtype | None = None) -> ArrayLike:
        # we need to explicitly call super() method as long as the `@overload`s
        #  are present in this file.
        return super().view(dtype)
