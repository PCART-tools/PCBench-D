    @_api.rename_parameter("3.6", "transOffset", "offset_transform")
    def set_offset_transform(self, offset_transform):
        """
        Set the artist offset transform.

        Parameters
        ----------
        offset_transform : `.Transform`
        """
        self._offset_transform = offset_transform
