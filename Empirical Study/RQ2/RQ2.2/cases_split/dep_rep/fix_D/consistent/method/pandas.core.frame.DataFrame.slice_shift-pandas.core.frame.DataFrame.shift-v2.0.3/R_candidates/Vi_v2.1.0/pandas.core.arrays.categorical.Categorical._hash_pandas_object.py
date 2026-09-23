    def _hash_pandas_object(
        self, *, encoding: str, hash_key: str, categorize: bool
    ) -> npt.NDArray[np.uint64]:
        """
        Hash a Categorical by hashing its categories, and then mapping the codes
        to the hashes.

        Parameters
        ----------
        encoding : str
        hash_key : str
        categorize : bool
            Ignored for Categorical.

        Returns
        -------
        np.ndarray[uint64]
        """
        # Note we ignore categorize, as we are already Categorical.
        from pandas.core.util.hashing import hash_array

        # Convert ExtensionArrays to ndarrays
        values = np.asarray(self.categories._values)
        hashed = hash_array(values, encoding, hash_key, categorize=False)

        # we have uint64, as we don't directly support missing values
        # we don't want to use take_nd which will coerce to float
        # instead, directly construct the result with a
        # max(np.uint64) as the missing value indicator
        #
        # TODO: GH#15362

        mask = self.isna()
        if len(hashed):
            result = hashed.take(self._codes)
        else:
            result = np.zeros(len(mask), dtype="uint64")

        if mask.any():
            result[mask] = lib.u8max

        return result
