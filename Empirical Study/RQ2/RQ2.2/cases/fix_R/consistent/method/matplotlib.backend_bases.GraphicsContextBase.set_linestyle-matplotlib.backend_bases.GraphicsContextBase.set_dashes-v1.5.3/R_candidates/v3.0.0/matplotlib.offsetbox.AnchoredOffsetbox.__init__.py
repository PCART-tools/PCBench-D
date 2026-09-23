    def __init__(self, loc,
                 pad=0.4, borderpad=0.5,
                 child=None, prop=None, frameon=True,
                 bbox_to_anchor=None,
                 bbox_transform=None,
                 **kwargs):
        """
        loc is a string or an integer specifying the legend location.
        The valid location codes are::

        'upper right'  : 1,
        'upper left'   : 2,
        'lower left'   : 3,
        'lower right'  : 4,
        'right'        : 5, (same as 'center right', for back-compatibility)
        'center left'  : 6,
        'center right' : 7,
        'lower center' : 8,
        'upper center' : 9,
        'center'       : 10,

        pad : pad around the child for drawing a frame. given in
          fraction of fontsize.

        borderpad : pad between offsetbox frame and the bbox_to_anchor,

        child : OffsetBox instance that will be anchored.

        prop : font property. This is only used as a reference for paddings.

        frameon : draw a frame box if True.

        bbox_to_anchor : bbox to anchor. Use self.axes.bbox if None.

        bbox_transform : with which the bbox_to_anchor will be transformed.

        """
        super().__init__(**kwargs)

        self.set_bbox_to_anchor(bbox_to_anchor, bbox_transform)
        self.set_child(child)

        if isinstance(loc, str):
            try:
                loc = self.codes[loc]
            except KeyError:
                raise ValueError('Unrecognized location "%s". Valid '
                                 'locations are\n\t%s\n'
                                 % (loc, '\n\t'.join(self.codes)))

        self.loc = loc
        self.borderpad = borderpad
        self.pad = pad

        if prop is None:
            self.prop = FontProperties(size=rcParams["legend.fontsize"])
        elif isinstance(prop, dict):
            self.prop = FontProperties(**prop)
            if "size" not in prop:
                self.prop.set_size(rcParams["legend.fontsize"])
        else:
            self.prop = prop

        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=self.prop.get_size_in_points(),
            snap=True
            )
        self.patch.set_boxstyle("square", pad=0)
        self._drawFrame = frameon
