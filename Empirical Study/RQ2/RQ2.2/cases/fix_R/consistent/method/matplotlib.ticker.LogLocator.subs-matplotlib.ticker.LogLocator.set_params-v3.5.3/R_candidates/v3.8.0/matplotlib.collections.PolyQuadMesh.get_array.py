    def get_array(self):
        # docstring inherited
        # Can remove this entire function once the deprecation period ends
        A = super().get_array()
        if A is None:
            return
        if self._deprecated_compression and np.any(np.ma.getmask(A)):
            _api.warn_deprecated("3.8", message=(
                "Getting the array from a PolyQuadMesh will return the full "
                "array in the future (uncompressed). To get this behavior now "
                "set the PolyQuadMesh with a 2D array .set_array(data2d)."))
            # Setting an array of a polycollection required
            # compressing the array
            return np.ma.compressed(A)
        return A
