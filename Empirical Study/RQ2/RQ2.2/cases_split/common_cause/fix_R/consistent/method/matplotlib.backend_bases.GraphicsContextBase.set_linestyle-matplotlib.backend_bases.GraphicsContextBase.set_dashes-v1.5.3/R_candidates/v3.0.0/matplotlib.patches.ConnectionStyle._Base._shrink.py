        def _shrink(self, path, shrinkA, shrinkB):
            """
            Shrink the path by fixed size (in points) with shrinkA and shrinkB
            """
            if shrinkA:
                x, y = path.vertices[0]
                insideA = inside_circle(x, y, shrinkA)

                try:
                    left, right = split_path_inout(path, insideA)
                    path = right
                except ValueError:
                    pass

            if shrinkB:
                x, y = path.vertices[-1]
                insideB = inside_circle(x, y, shrinkB)

                try:
                    left, right = split_path_inout(path, insideB)
                    path = left
                except ValueError:
                    pass

            return path
