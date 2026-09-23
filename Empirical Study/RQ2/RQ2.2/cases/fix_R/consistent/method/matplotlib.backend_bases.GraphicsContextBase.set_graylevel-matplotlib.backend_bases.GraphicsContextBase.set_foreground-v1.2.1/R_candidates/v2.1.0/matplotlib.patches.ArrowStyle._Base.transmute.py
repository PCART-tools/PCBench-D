        def transmute(self, path, mutation_size, linewidth):
            """
            The transmute method is the very core of the ArrowStyle
            class and must be overridden in the subclasses. It receives
            the path object along which the arrow will be drawn, and
            the mutation_size, with which the arrow head etc.
            will be scaled. The linewidth may be used to adjust
            the path so that it does not pass beyond the given
            points. It returns a tuple of a Path instance and a
            boolean. The boolean value indicate whether the path can
            be filled or not. The return value can also be a list of paths
            and list of booleans of a same length.
            """

            raise NotImplementedError('Derived must override')
