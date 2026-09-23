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
