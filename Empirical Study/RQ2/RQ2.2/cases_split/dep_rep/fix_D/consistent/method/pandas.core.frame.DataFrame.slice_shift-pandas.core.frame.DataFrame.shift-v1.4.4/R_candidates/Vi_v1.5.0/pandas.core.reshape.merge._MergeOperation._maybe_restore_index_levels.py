    def _maybe_restore_index_levels(self, result: DataFrame) -> None:
        """
        Restore index levels specified as `on` parameters

        Here we check for cases where `self.left_on` and `self.right_on` pairs
        each reference an index level in their respective DataFrames. The
        joined columns corresponding to these pairs are then restored to the
        index of `result`.

        **Note:** This method has side effects. It modifies `result` in-place

        Parameters
        ----------
        result: DataFrame
            merge result

        Returns
        -------
        None
        """
        names_to_restore = []
        for name, left_key, right_key in zip(
            self.join_names, self.left_on, self.right_on
        ):
            if (
                # Argument 1 to "_is_level_reference" of "NDFrame" has incompatible
                # type "Union[Hashable, ExtensionArray, Index, Series]"; expected
                # "Hashable"
                self.orig_left._is_level_reference(left_key)  # type: ignore[arg-type]
                # Argument 1 to "_is_level_reference" of "NDFrame" has incompatible
                # type "Union[Hashable, ExtensionArray, Index, Series]"; expected
                # "Hashable"
                and self.orig_right._is_level_reference(
                    right_key  # type: ignore[arg-type]
                )
                and left_key == right_key
                and name not in result.index.names
            ):

                names_to_restore.append(name)

        if names_to_restore:
            result.set_index(names_to_restore, inplace=True)
