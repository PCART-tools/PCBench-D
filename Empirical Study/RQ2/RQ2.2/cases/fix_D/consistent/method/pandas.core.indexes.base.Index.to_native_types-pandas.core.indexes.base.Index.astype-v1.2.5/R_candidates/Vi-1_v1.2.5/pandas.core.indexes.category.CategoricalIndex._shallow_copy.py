    @doc(Index._shallow_copy)
    def _shallow_copy(  # type:ignore[override]
        self,
        values: Optional[Categorical] = None,
        name: Label = no_default,
    ):
        name = self.name if name is no_default else name

        if values is not None:
            # In tests we only get here with Categorical objects that
            #  have matching .ordered, and values.categories a subset of
            #  our own.  However we do _not_ have a dtype match in general.
            values = Categorical(values, dtype=self.dtype)

        return super()._shallow_copy(values=values, name=name)
