    @classmethod
    def make_compound_path(cls, *args):
        """Make a compound path from a list of Path objects."""
        # Handle an empty list in args (i.e. no args).
        if not args:
            return Path(np.empty([0, 2], dtype=np.float32))

        lengths = [len(x) for x in args]
        total_length = sum(lengths)

        vertices = np.vstack([x.vertices for x in args])
        vertices.reshape((total_length, 2))

        codes = np.empty(total_length, dtype=cls.code_type)
        i = 0
        for path in args:
            if path.codes is None:
                codes[i] = cls.MOVETO
                codes[i + 1:i + len(path.vertices)] = cls.LINETO
            else:
                codes[i:i + len(path.codes)] = path.codes
            i += len(path.vertices)

        return cls(vertices, codes)
