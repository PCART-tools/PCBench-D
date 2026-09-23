        def __call__(self, posA, posB,
                     shrinkA=2., shrinkB=2., patchA=None, patchB=None):
            """
            Call the *connect* method to create a path between *posA* and
            *posB*; then clip and shrink the path.
            """
            path = self.connect(posA, posB)
            clipped_path = self._clip(path, patchA, patchB)
            shrunk_path = self._shrink(clipped_path, shrinkA, shrinkB)
            return shrunk_path
