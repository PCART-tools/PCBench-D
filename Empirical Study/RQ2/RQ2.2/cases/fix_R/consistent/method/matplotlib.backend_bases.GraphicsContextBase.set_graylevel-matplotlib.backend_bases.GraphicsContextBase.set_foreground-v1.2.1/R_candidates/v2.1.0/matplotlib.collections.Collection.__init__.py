    def __init__(self,
                 edgecolors=None,
                 facecolors=None,
                 linewidths=None,
                 linestyles='solid',
                 antialiaseds=None,
                 offsets=None,
                 transOffset=None,
                 norm=None,  # optional for ScalarMappable
                 cmap=None,  # ditto
                 pickradius=5.0,
                 hatch=None,
                 urls=None,
                 offset_position='screen',
                 zorder=1,
                 **kwargs
                 ):
        """
        Create a Collection

        %(Collection)s
        """
        artist.Artist.__init__(self)
        cm.ScalarMappable.__init__(self, norm, cmap)
        # list of un-scaled dash patterns
        # this is needed scaling the dash pattern by linewidth
        self._us_linestyles = [(None, None)]
        # list of dash patterns
        self._linestyles = [(None, None)]
        # list of unbroadcast/scaled linewidths
        self._us_lw = [0]
        self._linewidths = [0]
        self._is_filled = True  # May be modified by set_facecolor().

        self._hatch_color = mcolors.to_rgba(mpl.rcParams['hatch.color'])
        self.set_facecolor(facecolors)
        self.set_edgecolor(edgecolors)
        self.set_linewidth(linewidths)
        self.set_linestyle(linestyles)
        self.set_antialiased(antialiaseds)
        self.set_pickradius(pickradius)
        self.set_urls(urls)
        self.set_hatch(hatch)
        self.set_offset_position(offset_position)
        self.set_zorder(zorder)

        self._offsets = np.zeros((1, 2))
        self._uniform_offsets = None
        if offsets is not None:
            offsets = np.asanyarray(offsets, float)
            # Broadcast (2,) -> (1, 2) but nothing else.
            if offsets.shape == (2,):
                offsets = offsets[None, :]
            if transOffset is not None:
                self._offsets = offsets
                self._transOffset = transOffset
            else:
                self._uniform_offsets = offsets

        self._path_effects = None
        self.update(kwargs)
        self._paths = None
