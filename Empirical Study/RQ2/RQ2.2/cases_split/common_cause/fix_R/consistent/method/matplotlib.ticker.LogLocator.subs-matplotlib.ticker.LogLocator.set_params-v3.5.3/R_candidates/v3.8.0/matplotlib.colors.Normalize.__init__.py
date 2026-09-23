    def __init__(self, vmin=None, vmax=None, clip=False):
        """
        Parameters
        ----------
        vmin, vmax : float or None
            If *vmin* and/or *vmax* is not given, they are initialized from the
            minimum and maximum value, respectively, of the first input
            processed; i.e., ``__call__(A)`` calls ``autoscale_None(A)``.

        clip : bool, default: False
            Determines the behavior for mapping values outside the range
            ``[vmin, vmax]``.

            If clipping is off, values outside the range ``[vmin, vmax]`` are also
            transformed linearly, resulting in values outside ``[0, 1]``. For a
            standard use with colormaps, this behavior is desired because colormaps
            mark these outside values with specific colors for *over* or *under*.

            If ``True`` values falling outside the range ``[vmin, vmax]``,
            are mapped to 0 or 1, whichever is closer. This makes these values
            indistinguishable from regular boundary values and can lead to
            misinterpretation of the data.

        Notes
        -----
        Returns 0 if ``vmin == vmax``.
        """
        self._vmin = _sanitize_extrema(vmin)
        self._vmax = _sanitize_extrema(vmax)
        self._clip = clip
        self._scale = None
        self.callbacks = cbook.CallbackRegistry(signals=["changed"])
