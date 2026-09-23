    def _convert_listlike_indexer(self, keyarr) -> np.ndarray | None:
        """
        Analogous to get_indexer when we are partial-indexing on our first level.

        Parameters
        ----------
        keyarr : Index, np.ndarray, or ExtensionArray
            Indexer to convert.

        Returns
        -------
        np.ndarray[intp] or None
        """
        indexer = None

        # are we indexing a specific level
        if len(keyarr) and not isinstance(keyarr[0], tuple):
            _, indexer = self.reindex(keyarr, level=0)

            # take all
            if indexer is None:
                indexer = np.arange(len(self), dtype=np.intp)
                return indexer

            check = self.levels[0].get_indexer(keyarr)
            mask = check == -1
            if mask.any():
                raise KeyError(f"{keyarr[mask]} not in index")
            elif is_empty_indexer(indexer, keyarr):
                # We get here when levels still contain values which are not
                # actually in Index anymore
                raise KeyError(f"{keyarr} not in index")

        return indexer
