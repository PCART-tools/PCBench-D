    def set_family(self, family):
        """
        Change the font family.  May be either an alias (generic name
        is CSS parlance), such as: 'serif', 'sans-serif', 'cursive',
        'fantasy', or 'monospace', a real font name or a list of real
        font names.  Real font names are not supported when
        :rc:`text.usetex` is `True`. Default: :rc:`font.family`
        """
        if family is None:
            family = mpl.rcParams['font.family']
        if isinstance(family, str):
            family = [family]
        self._family = family
