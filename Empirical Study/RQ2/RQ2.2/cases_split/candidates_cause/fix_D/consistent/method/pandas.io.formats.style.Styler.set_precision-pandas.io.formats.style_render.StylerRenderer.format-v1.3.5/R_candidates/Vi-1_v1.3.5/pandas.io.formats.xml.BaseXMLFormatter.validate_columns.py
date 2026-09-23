    def validate_columns(self) -> None:
        """
        Validate elems_cols and attrs_cols.

        This method will check if columns is list-like.

        Raises
        ------
        ValueError
            * If value is not a list and less then length of nodes.
        """
        if self.attr_cols and not is_list_like(self.attr_cols):
            raise TypeError(
                f"{type(self.attr_cols).__name__} is not a valid type for attr_cols"
            )

        if self.elem_cols and not is_list_like(self.elem_cols):
            raise TypeError(
                f"{type(self.elem_cols).__name__} is not a valid type for elem_cols"
            )
