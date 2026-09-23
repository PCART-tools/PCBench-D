    def _replace_columnwise(
        self, mapping: dict[Hashable, tuple[Any, Any]], inplace: bool, regex
    ):
        """
        Dispatch to Series.replace column-wise.

        Parameters
        ----------
        mapping : dict
            of the form {col: (target, value)}
        inplace : bool
        regex : bool or same types as `to_replace` in DataFrame.replace

        Returns
        -------
        DataFrame or None
        """
        # Operate column-wise
        res = self if inplace else self.copy()
        ax = self.columns

        for i in range(len(ax)):
            if ax[i] in mapping:
                ser = self.iloc[:, i]

                target, value = mapping[ax[i]]
                newobj = ser.replace(target, value, regex=regex)

                res.iloc[:, i] = newobj

        if inplace:
            return
        return res.__finalize__(self)
