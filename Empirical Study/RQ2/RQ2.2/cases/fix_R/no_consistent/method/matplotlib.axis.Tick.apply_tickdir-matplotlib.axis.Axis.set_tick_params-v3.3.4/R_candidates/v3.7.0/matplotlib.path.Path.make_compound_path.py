    @classmethod
    def make_compound_path(cls, *args):
        """
        Make a compound path from a list of `Path` objects. Blindly removes
        all `Path.STOP` control points.
        """
        # Handle an empty list in args (i.e. no args).
        if not args:
            return Path(np.empty([0, 2], dtype=np.float32))
        vertices = np.concatenate([x.vertices for x in args])
        codes = np.empty(len(vertices), dtype=cls.code_type)
        i = 0
        for path in args:
            if path.codes is None:
                codes[i] = cls.MOVETO
                codes[i + 1:i + len(path.vertices)] = cls.LINETO
            else:
                codes[i:i + len(path.codes)] = path.codes
            i += len(path.vertices)
        # remove STOP's, since internal STOPs are a bug
        not_stop_mask = codes != cls.STOP
        vertices = vertices[not_stop_mask, :]
        codes = codes[not_stop_mask]

        return cls(vertices, codes)
