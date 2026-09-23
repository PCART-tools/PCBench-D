    @staticmethod
    def _total_to_compress_renum(mask, n=None):
        """
        Parameters
        ----------
        mask : 1d boolean array or None
            mask
        n : integer
            length of the mask. Useful only id mask can be None

        Returns
        -------
        renum : integer array
            array so that (`valid_array` being a compressed array
            based on a `masked_array` with mask *mask*) :

                  - For all i such as mask[i] = False:
                    valid_array[renum[i]] = masked_array[i]
                  - For all i such as mask[i] = True:
                    renum[i] = -1 (invalid value)

        """
        if n is None:
            n = np.size(mask)
        if mask is not None:
            renum = np.full(n, -1, dtype=np.int32)  # Default num is -1
            valid = np.arange(n, dtype=np.int32)[~mask]
            renum[valid] = np.arange(np.size(valid, 0), dtype=np.int32)
            return renum
        else:
            return np.arange(n, dtype=np.int32)
