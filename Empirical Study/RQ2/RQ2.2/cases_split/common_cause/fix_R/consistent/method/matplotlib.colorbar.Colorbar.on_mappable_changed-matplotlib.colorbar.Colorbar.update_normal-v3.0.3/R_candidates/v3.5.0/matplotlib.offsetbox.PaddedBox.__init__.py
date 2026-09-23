    def __init__(self, child, pad=None, draw_frame=False, patch_attrs=None):
        """
        Parameters
        ----------
        child : `~matplotlib.artist.Artist`
            The contained `.Artist`.
        pad : float
            The padding in points. This will be scaled with the renderer dpi.
            In contrast *width* and *height* are in *pixels* and thus not
            scaled.
        draw_frame : bool
            Whether to draw the contained `.FancyBboxPatch`.
        patch_attrs : dict or None
            Additional parameters passed to the contained `.FancyBboxPatch`.
        """
        super().__init__()
        self.pad = pad
        self._children = [child]
        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=1,  # self.prop.get_size_in_points(),
            snap=True,
            visible=draw_frame,
            boxstyle="square,pad=0",
        )
        if patch_attrs is not None:
            self.patch.update(patch_attrs)
