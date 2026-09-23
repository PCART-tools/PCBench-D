    def _validate_codes(self, level: list, code: list):
        """
        Reassign code values as -1 if their corresponding levels are NaN.

        Parameters
        ----------
        code : list
            Code to reassign.
        level : list
            Level to check for missing values (NaN, NaT, None).

        Returns
        -------
        new code where code value = -1 if it corresponds
        to a level with missing values (NaN, NaT, None).
        """
        null_mask = isna(level)
        if np.any(null_mask):
            # Incompatible types in assignment (expression has type
            # "ndarray[Any, dtype[Any]]", variable has type "List[Any]")
            code = np.where(null_mask[code], -1, code)  # type: ignore[assignment]
        return code
