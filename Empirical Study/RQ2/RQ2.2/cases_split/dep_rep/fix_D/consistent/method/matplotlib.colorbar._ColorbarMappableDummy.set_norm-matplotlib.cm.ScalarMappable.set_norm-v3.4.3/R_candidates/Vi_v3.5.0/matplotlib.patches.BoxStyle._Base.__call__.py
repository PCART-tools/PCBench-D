        def __call__(self, x0, y0, width, height, mutation_size):
            """
            Given the location and size of the box, return the path of
            the box around it.

            Parameters
            ----------
            x0, y0, width, height : float
                Location and size of the box.
            mutation_size : float
                A reference scale for the mutation.

            Returns
            -------
            `~matplotlib.path.Path`
            """
            raise NotImplementedError('Derived must override')
