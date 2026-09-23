    def __getitem__(self, item: str | int) -> Expr:
        if isinstance(item, str):
            return self.field(item)
        elif isinstance(item, int):
            return wrap_expr(self._pyexpr.struct_field_by_index(item))
        else:
            raise TypeError(
                f"expected type 'int | str', got {type(item).__name__!r} ({item!r})"
            )
