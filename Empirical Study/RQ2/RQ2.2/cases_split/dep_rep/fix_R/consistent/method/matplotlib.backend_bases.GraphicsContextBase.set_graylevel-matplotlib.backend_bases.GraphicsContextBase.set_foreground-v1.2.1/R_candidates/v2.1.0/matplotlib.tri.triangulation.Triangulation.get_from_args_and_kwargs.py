    @staticmethod
    def get_from_args_and_kwargs(*args, **kwargs):
        """
        Return a Triangulation object from the args and kwargs, and
        the remaining args and kwargs with the consumed values removed.

        There are two alternatives: either the first argument is a
        Triangulation object, in which case it is returned, or the args
        and kwargs are sufficient to create a new Triangulation to
        return.  In the latter case, see Triangulation.__init__ for
        the possible args and kwargs.
        """
        if isinstance(args[0], Triangulation):
            triangulation = args[0]
            args = args[1:]
        else:
            x = args[0]
            y = args[1]
            args = args[2:]  # Consumed first two args.

            # Check triangles in kwargs then args.
            triangles = kwargs.pop('triangles', None)
            from_args = False
            if triangles is None and len(args) > 0:
                triangles = args[0]
                from_args = True

            if triangles is not None:
                try:
                    triangles = np.asarray(triangles, dtype=np.int32)
                except ValueError:
                    triangles = None

            if triangles is not None and (triangles.ndim != 2 or
                                          triangles.shape[1] != 3):
                triangles = None

            if triangles is not None and from_args:
                args = args[1:]  # Consumed first item in args.

            # Check for mask in kwargs.
            mask = kwargs.pop('mask', None)

            triangulation = Triangulation(x, y, triangles, mask)
        return triangulation, args, kwargs
