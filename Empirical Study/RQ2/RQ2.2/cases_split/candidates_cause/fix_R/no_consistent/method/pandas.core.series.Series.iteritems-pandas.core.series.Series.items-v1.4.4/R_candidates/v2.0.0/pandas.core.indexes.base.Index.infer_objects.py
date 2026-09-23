    def infer_objects(self, copy: bool = True) -> Index:
        """
        If we have an object dtype, try to infer a non-object dtype.

        Parameters
        ----------
        copy : bool, default True
            Whether to make a copy in cases where no inference occurs.
        """
        if self._is_multi:
            raise NotImplementedError(
                "infer_objects is not implemented for MultiIndex. "
                "Use index.to_frame().infer_objects() instead."
            )
        if self.dtype != object:
            return self.copy() if copy else self

        values = self._values
        values = cast("npt.NDArray[np.object_]", values)
        res_values = lib.maybe_convert_objects(
            values,
            convert_datetime=True,
            convert_timedelta=True,
            convert_period=True,
            convert_interval=True,
        )
        if copy and res_values is values:
            return self.copy()
        result = Index(res_values, name=self.name)
        if not copy and res_values is values and self._references is not None:
            result._references = self._references
            result._references.add_index_reference(result)
        return result
