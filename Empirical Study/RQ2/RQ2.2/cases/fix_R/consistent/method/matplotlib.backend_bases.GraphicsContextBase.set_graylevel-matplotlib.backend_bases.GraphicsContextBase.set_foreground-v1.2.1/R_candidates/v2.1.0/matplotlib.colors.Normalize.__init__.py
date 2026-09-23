    def __init__(self, vmin=None, vmax=None, clip=False):
        """
        If *vmin* or *vmax* is not given, they are initialized from the
        minimum and maximum value respectively of the first input
        processed.  That is, *__call__(A)* calls *autoscale_None(A)*.
        If *clip* is *True* and the given value falls outside the range,
        the returned value will be 0 or 1, whichever is closer.
        Returns 0 if::

            vmin==vmax

        Works with scalars or arrays, including masked arrays.  If
        *clip* is *True*, masked values are set to 1; otherwise they
        remain masked.  Clipping silently defeats the purpose of setting
        the over, under, and masked colors in the colormap, so it is
        likely to lead to surprises; therefore the default is
        *clip* = *False*.
        """
        self.vmin = vmin
        self.vmax = vmax
        self.clip = clip
