    class _Base:
        """
        A base class for connectionstyle classes. The subclass needs
        to implement a *connect* method whose call signature is::

          connect(posA, posB)

        where posA and posB are tuples of x, y coordinates to be
        connected.  The method needs to return a path connecting two
        points. This base class defines a __call__ method, and a few
        helper methods.
        """

        class SimpleEvent:
            def __init__(self, xy):
                self.x, self.y = xy

        def _clip(self, path, patchA, patchB):
            """
            Clip the path to the boundary of the patchA and patchB.
            The starting point of the path needed to be inside of the
            patchA and the end point inside the patch B. The *contains*
            methods of each patch object is utilized to test if the point
            is inside the path.
            """

            if patchA:
                def insideA(xy_display):
                    xy_event = ConnectionStyle._Base.SimpleEvent(xy_display)
                    return patchA.contains(xy_event)[0]

                try:
                    left, right = split_path_inout(path, insideA)
                except ValueError:
                    right = path

                path = right

            if patchB:
                def insideB(xy_display):
                    xy_event = ConnectionStyle._Base.SimpleEvent(xy_display)
                    return patchB.contains(xy_event)[0]

                try:
                    left, right = split_path_inout(path, insideB)
                except ValueError:
                    left = path

                path = left

            return path

        def _shrink(self, path, shrinkA, shrinkB):
            """
            Shrink the path by fixed size (in points) with shrinkA and shrinkB.
            """
            if shrinkA:
                insideA = inside_circle(*path.vertices[0], shrinkA)
                try:
                    left, path = split_path_inout(path, insideA)
                except ValueError:
                    pass
            if shrinkB:
                insideB = inside_circle(*path.vertices[-1], shrinkB)
                try:
                    path, right = split_path_inout(path, insideB)
                except ValueError:
                    pass
            return path

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
