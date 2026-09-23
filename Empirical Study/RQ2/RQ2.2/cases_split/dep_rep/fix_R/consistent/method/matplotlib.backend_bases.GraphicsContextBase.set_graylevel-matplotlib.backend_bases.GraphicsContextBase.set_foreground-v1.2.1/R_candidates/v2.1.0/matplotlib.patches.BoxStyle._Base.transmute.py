        def transmute(self, x0, y0, width, height, mutation_size):
            """
            The transmute method is a very core of the
            :class:`BboxTransmuter` class and must be overridden in the
            subclasses. It receives the location and size of the
            rectangle, and the mutation_size, with which the amount of
            padding and etc. will be scaled. It returns a
            :class:`~matplotlib.path.Path` instance.
            """
            raise NotImplementedError('Derived must override')
