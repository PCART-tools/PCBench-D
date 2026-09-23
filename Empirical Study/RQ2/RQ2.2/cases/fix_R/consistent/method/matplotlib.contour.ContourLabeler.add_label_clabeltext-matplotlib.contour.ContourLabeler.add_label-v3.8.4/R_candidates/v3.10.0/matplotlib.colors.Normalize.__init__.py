    def __init__(self, vmin=None, vmax=None, clip=False):
        """
        Parameters
        ----------
        vmin, vmax : float or None
            Values within the range ``[vmin, vmax]`` from the input data will be
            linearly mapped to ``[0, 1]``. If either *vmin* or *vmax* is not
            provided, they default to the minimum and maximum values of the input,
            respectively.

        clip : bool, default: False
            Determines the behavior for mapping values outside the range
            ``[vmin, vmax]``.

            If clipping is off, values outside the range ``[vmin, vmax]`` are
            also transformed, resulting in values outside ``[0, 1]``.  This
            behavior is usually desirable, as colormaps can mark these *under*
            and *over* values with specific colors.

            If clipping is on, values below *vmin* are mapped to 0 and values
            above *vmax* are mapped to 1. Such values become indistinguishable
            from regular boundary values, which may cause misinterpretation of
            the data.

        Notes
        -----
        If ``vmin == vmax``, input data will be mapped to 0.
        """
        self._vmin = _sanitize_extrema(vmin)
        self._vmax = _sanitize_extrema(vmax)
        self._clip = clip
        self._scale = None
        self.callbacks = cbook.CallbackRegistry(signals=["changed"])
