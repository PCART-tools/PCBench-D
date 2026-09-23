    def __new__(cls, stylename, **kw):
        """
        return the instance of the subclass with the given style name.
        """

        # The "class" should have the _style_list attribute, which is a mapping
        # of style names to style classes.

        _list = stylename.replace(" ", "").split(",")
        _name = _list[0].lower()
        try:
            _cls = cls._style_list[_name]
        except KeyError:
            raise ValueError("Unknown style : %s" % stylename)

        try:
            _args_pair = [cs.split("=") for cs in _list[1:]]
            _args = {k: float(v) for k, v in _args_pair}
        except ValueError:
            raise ValueError("Incorrect style argument : %s" % stylename)
        _args.update(kw)

        return _cls(**_args)
