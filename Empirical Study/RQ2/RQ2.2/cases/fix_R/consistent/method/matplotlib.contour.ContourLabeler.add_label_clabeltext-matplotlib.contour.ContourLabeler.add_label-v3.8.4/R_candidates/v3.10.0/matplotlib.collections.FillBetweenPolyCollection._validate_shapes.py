    @staticmethod
    def _validate_shapes(t_dir, f_dir, t, f1, f2):
        """Validate that t, f1 and f2 are 1-dimensional and have the same length."""
        names = (d + s for d, s in zip((t_dir, f_dir, f_dir), ("", "1", "2")))
        for name, array in zip(names, [t, f1, f2]):
            if array.ndim > 1:
                raise ValueError(f"{name!r} is not 1-dimensional")
            if t.size > 1 and array.size > 1 and t.size != array.size:
                msg = "{!r} has size {}, but {!r} has an unequal size of {}".format(
                    t_dir, t.size, name, array.size)
                raise ValueError(msg)
