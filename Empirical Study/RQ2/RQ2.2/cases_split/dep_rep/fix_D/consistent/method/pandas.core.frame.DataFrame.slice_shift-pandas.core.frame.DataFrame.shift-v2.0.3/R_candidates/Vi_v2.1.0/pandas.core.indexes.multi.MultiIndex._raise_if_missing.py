    def _raise_if_missing(self, key, indexer, axis_name: str) -> None:
        keyarr = key
        if not isinstance(key, Index):
            keyarr = com.asarray_tuplesafe(key)

        if len(keyarr) and not isinstance(keyarr[0], tuple):
            # i.e. same condition for special case in MultiIndex._get_indexer_strict

            mask = indexer == -1
            if mask.any():
                check = self.levels[0].get_indexer(keyarr)
                cmask = check == -1
                if cmask.any():
                    raise KeyError(f"{keyarr[cmask]} not in index")
                # We get here when levels still contain values which are not
                # actually in Index anymore
                raise KeyError(f"{keyarr} not in index")
        else:
            return super()._raise_if_missing(key, indexer, axis_name)
