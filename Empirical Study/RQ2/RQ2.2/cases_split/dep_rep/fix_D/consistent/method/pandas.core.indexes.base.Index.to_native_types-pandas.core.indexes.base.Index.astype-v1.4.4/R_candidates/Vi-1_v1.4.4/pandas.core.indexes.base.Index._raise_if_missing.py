    def _raise_if_missing(self, key, indexer, axis_name: str_t) -> None:
        """
        Check that indexer can be used to return a result.

        e.g. at least one element was found,
        unless the list of keys was actually empty.

        Parameters
        ----------
        key : list-like
            Targeted labels (only used to show correct error message).
        indexer: array-like of booleans
            Indices corresponding to the key,
            (with -1 indicating not found).
        axis_name : str

        Raises
        ------
        KeyError
            If at least one key was requested but none was found.
        """
        if len(key) == 0:
            return

        # Count missing values
        missing_mask = indexer < 0
        nmissing = missing_mask.sum()

        if nmissing:

            # TODO: remove special-case; this is just to keep exception
            #  message tests from raising while debugging
            use_interval_msg = is_interval_dtype(self.dtype) or (
                is_categorical_dtype(self.dtype)
                # "Index" has no attribute "categories"  [attr-defined]
                and is_interval_dtype(
                    self.categories.dtype  # type: ignore[attr-defined]
                )
            )

            if nmissing == len(indexer):
                if use_interval_msg:
                    key = list(key)
                raise KeyError(f"None of [{key}] are in the [{axis_name}]")

            not_found = list(ensure_index(key)[missing_mask.nonzero()[0]].unique())
            raise KeyError(f"{not_found} not in index")
