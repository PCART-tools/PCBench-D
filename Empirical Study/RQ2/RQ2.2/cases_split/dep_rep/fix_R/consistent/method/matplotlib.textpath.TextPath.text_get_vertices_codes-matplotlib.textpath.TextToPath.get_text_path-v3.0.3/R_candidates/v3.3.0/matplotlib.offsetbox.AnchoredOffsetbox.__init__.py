    def __init__(self, loc,
                 pad=0.4, borderpad=0.5,
                 child=None, prop=None, frameon=True,
                 bbox_to_anchor=None,
                 bbox_transform=None,
                 **kwargs):
        """
        Parameters
        ----------
        loc : str
            The box location. Supported values:

            - 'upper right'
            - 'upper left'
            - 'lower left'
            - 'lower right'
            - 'center left'
            - 'center right'
            - 'lower center'
            - 'upper center'
            - 'center'

            For backward compatibility, numeric values are accepted as well.
            See the parameter *loc* of `.Legend` for details.

        pad : float, default: 0.4
            Padding around the child as fraction of the fontsize.

        borderpad : float, default: 0.5
            Padding between the offsetbox frame and the *bbox_to_anchor*.

        child : `.OffsetBox`
            The box that will be anchored.

        prop : `.FontProperties`
            This is only used as a reference for paddings. If not given,
            :rc:`legend.fontsize` is used.

        frameon : bool
            Whether to draw a frame around the box.

        bbox_to_anchor : `.BboxBase`, 2-tuple, or 4-tuple of floats
            Box that is used to position the legend in conjunction with *loc*.

        bbox_transform : None or :class:`matplotlib.transforms.Transform`
            The transform for the bounding box (*bbox_to_anchor*).

        **kwargs
            All other parameters are passed on to `.OffsetBox`.

        Notes
        -----
        See `.Legend` for a detailed description of the anchoring mechanism.
        """
        super().__init__(**kwargs)

        self.set_bbox_to_anchor(bbox_to_anchor, bbox_transform)
        self.set_child(child)

        if isinstance(loc, str):
            loc = cbook._check_getitem(self.codes, loc=loc)

        self.loc = loc
        self.borderpad = borderpad
        self.pad = pad

        if prop is None:
            self.prop = FontProperties(size=rcParams["legend.fontsize"])
        else:
            self.prop = FontProperties._from_any(prop)
            if isinstance(prop, dict) and "size" not in prop:
                self.prop.set_size(rcParams["legend.fontsize"])

        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=self.prop.get_size_in_points(),
            snap=True,
            visible=frameon,
            boxstyle="square,pad=0",
        )
