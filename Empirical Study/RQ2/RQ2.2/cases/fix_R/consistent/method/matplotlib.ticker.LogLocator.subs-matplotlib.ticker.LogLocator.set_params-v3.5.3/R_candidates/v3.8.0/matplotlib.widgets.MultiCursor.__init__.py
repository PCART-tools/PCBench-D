    def __init__(self, canvas, axes, *, useblit=True, horizOn=False, vertOn=True,
                 **lineprops):
        # canvas is stored only to provide the deprecated .canvas attribute;
        # once it goes away the unused argument won't need to be stored at all.
        self._canvas = canvas

        self.axes = axes
        self.horizOn = horizOn
        self.vertOn = vertOn

        self._canvas_infos = {
            ax.figure.canvas: {"cids": [], "background": None} for ax in axes}

        xmin, xmax = axes[-1].get_xlim()
        ymin, ymax = axes[-1].get_ylim()
        xmid = 0.5 * (xmin + xmax)
        ymid = 0.5 * (ymin + ymax)

        self.visible = True
        self.useblit = (
            useblit
            and all(canvas.supports_blit for canvas in self._canvas_infos))

        if self.useblit:
            lineprops['animated'] = True

        self.vlines = [ax.axvline(xmid, visible=False, **lineprops)
                       for ax in axes]
        self.hlines = [ax.axhline(ymid, visible=False, **lineprops)
                       for ax in axes]

        self.connect()
