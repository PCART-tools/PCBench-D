class ColorSequenceRegistry(Mapping):
    r"""
    Container for sequences of colors that are known to Matplotlib by name.

    The universal registry instance is `matplotlib.color_sequences`. There
    should be no need for users to instantiate `.ColorSequenceRegistry`
    themselves.

    Read access uses a dict-like interface mapping names to lists of colors::

        import matplotlib as mpl
        cmap = mpl.color_sequences['tab10']

    The returned lists are copies, so that their modification does not change
    the global definition of the color sequence.

    Additional color sequences can be added via
    `.ColorSequenceRegistry.register`::

        mpl.color_sequences.register('rgb', ['r', 'g', 'b'])
    """

    _BUILTIN_COLOR_SEQUENCES = {
        'tab10': _cm._tab10_data,
        'tab20': _cm._tab20_data,
        'tab20b': _cm._tab20b_data,
        'tab20c': _cm._tab20c_data,
        'Pastel1': _cm._Pastel1_data,
        'Pastel2': _cm._Pastel2_data,
        'Paired': _cm._Paired_data,
        'Accent': _cm._Accent_data,
        'Dark2': _cm._Dark2_data,
        'Set1': _cm._Set1_data,
        'Set2': _cm._Set1_data,
        'Set3': _cm._Set1_data,
    }

    def __init__(self):
        self._color_sequences = {**self._BUILTIN_COLOR_SEQUENCES}

    def __getitem__(self, item):
        try:
            return list(self._color_sequences[item])
        except KeyError:
            raise KeyError(f"{item!r} is not a known color sequence name")

    def __iter__(self):
        return iter(self._color_sequences)

    def __len__(self):
        return len(self._color_sequences)

    def __str__(self):
        return ('ColorSequenceRegistry; available colormaps:\n' +
                ', '.join(f"'{name}'" for name in self))

    def register(self, name, color_list):
        """
        Register a new color sequence.

        The color sequence registry stores a copy of the given *color_list*, so
        that future changes to the original list do not affect the registered
        color sequence. Think of this as the registry taking a snapshot
        of *color_list* at registration.

        Parameters
        ----------
        name : str
            The name for the color sequence.

        color_list : list of colors
            An iterable returning valid Matplotlib colors when iterating over.
            Note however that the returned color sequence will always be a
            list regardless of the input type.

        """
        if name in self._BUILTIN_COLOR_SEQUENCES:
            raise ValueError(f"{name!r} is a reserved name for a builtin "
                             "color sequence")

        color_list = list(color_list)  # force copy and coerce type to list
        for color in color_list:
            try:
                to_rgba(color)
            except ValueError:
                raise ValueError(
                    f"{color!r} is not a valid color specification")

        self._color_sequences[name] = color_list

    def unregister(self, name):
        """
        Remove a sequence from the registry.

        You cannot remove built-in color sequences.

        If the name is not registered, returns with no error.
        """
        if name in self._BUILTIN_COLOR_SEQUENCES:
            raise ValueError(
                f"Cannot unregister builtin color sequence {name!r}")
        self._color_sequences.pop(name, None)
