    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def argsort(
        self,
        ascending: bool = True,
        kind: str = "quicksort",
        na_position: str = "last",
        *args,
        **kwargs,
    ) -> np.ndarray:
        ascending = nv.validate_argsort_with_ascending(ascending, args, kwargs)

        if ascending and kind == "quicksort" and na_position == "last":
            return np.lexsort((self.right, self.left))

        # TODO: other cases we can use lexsort for?  much more performant.
        return super().argsort(
            ascending=ascending, kind=kind, na_position=na_position, **kwargs
        )
