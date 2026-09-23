    def to_dense(self, fill=None):
        """
        Convert SparseArray to a NumPy array.

        Parameters
        ----------
        fill: float, default None
            .. deprecated:: 0.20.0
               This argument is not respected by this function.

        Returns
        -------
        arr : NumPy array
        """
        if fill is not None:
            warnings.warn(("The 'fill' parameter has been deprecated and "
                           "will be removed in a future version."),
                          FutureWarning, stacklevel=2)
        return self.values
