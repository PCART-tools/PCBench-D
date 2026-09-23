    def __init__(self,
                 edgecolor=None,
                 facecolor=None,
                 color=None,
                 linewidth=None,
                 linestyle=None,
                 antialiased=None,
                 hatch=None,
                 fill=True,
                 capstyle=None,
                 joinstyle=None,
                 **kwargs):
        """
        The following kwarg properties are supported

        %(Patch)s
        """
        artist.Artist.__init__(self)

        if linewidth is None:
            linewidth = mpl.rcParams['patch.linewidth']
        if linestyle is None:
            linestyle = "solid"
        if capstyle is None:
            capstyle = 'butt'
        if joinstyle is None:
            joinstyle = 'miter'
        if antialiased is None:
            antialiased = mpl.rcParams['patch.antialiased']

        self._hatch_color = colors.to_rgba(mpl.rcParams['hatch.color'])
        self._fill = True  # needed for set_facecolor call
        if color is not None:
            if edgecolor is not None or facecolor is not None:
                warnings.warn("Setting the 'color' property will override"
                              "the edgecolor or facecolor properties.")
            self.set_color(color)
        else:
            self.set_edgecolor(edgecolor)
            self.set_facecolor(facecolor)
        # unscaled dashes.  Needed to scale dash patterns by lw
        self._us_dashes = None
        self._linewidth = 0

        self.set_fill(fill)
        self.set_linestyle(linestyle)
        self.set_linewidth(linewidth)
        self.set_antialiased(antialiased)
        self.set_hatch(hatch)
        self.set_capstyle(capstyle)
        self.set_joinstyle(joinstyle)
        self._combined_transform = transforms.IdentityTransform()

        if len(kwargs):
            self.update(kwargs)
