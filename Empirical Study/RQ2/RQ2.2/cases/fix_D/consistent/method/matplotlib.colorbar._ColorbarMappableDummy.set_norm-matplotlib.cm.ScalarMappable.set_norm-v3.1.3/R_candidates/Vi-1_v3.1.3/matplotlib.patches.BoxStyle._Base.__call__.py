        def __call__(self, x0, y0, width, height, mutation_size,
                     aspect_ratio=1.):
            """
            Given the location and size of the box, return the path of
            the box around it.

              - *x0*, *y0*, *width*, *height* : location and size of the box
              - *mutation_size* : a reference scale for the mutation.
              - *aspect_ratio* : aspect-ration for the mutation.
            """
            # The __call__ method is a thin wrapper around the transmute method
            # and takes care of the aspect.

            if aspect_ratio is not None:
                # Squeeze the given height by the aspect_ratio
                y0, height = y0 / aspect_ratio, height / aspect_ratio
                # call transmute method with squeezed height.
                path = self.transmute(x0, y0, width, height, mutation_size)
                vertices, codes = path.vertices, path.codes
                # Restore the height
                vertices[:, 1] = vertices[:, 1] * aspect_ratio
                return Path(vertices, codes)
            else:
                return self.transmute(x0, y0, width, height, mutation_size)
