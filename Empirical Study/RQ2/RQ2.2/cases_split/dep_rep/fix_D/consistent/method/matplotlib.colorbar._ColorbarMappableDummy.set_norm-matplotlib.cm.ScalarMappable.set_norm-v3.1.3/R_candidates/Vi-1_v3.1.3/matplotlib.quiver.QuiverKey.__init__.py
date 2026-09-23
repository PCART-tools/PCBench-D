    def __init__(self, Q, X, Y, U, label,
                 *, angle=0, coordinates='axes', color=None, labelsep=0.1,
                 labelpos='N', labelcolor=None, fontproperties=None,
                 **kw):
        martist.Artist.__init__(self)
        self.Q = Q
        self.X = X
        self.Y = Y
        self.U = U
        self.angle = angle
        self.coord = coordinates
        self.color = color
        self.label = label
        self._labelsep_inches = labelsep
        self.labelsep = (self._labelsep_inches * Q.ax.figure.dpi)

        # try to prevent closure over the real self
        weak_self = weakref.ref(self)

        def on_dpi_change(fig):
            self_weakref = weak_self()
            if self_weakref is not None:
                self_weakref.labelsep = (self_weakref._labelsep_inches*fig.dpi)
                self_weakref._initialized = False  # simple brute force update
                                                   # works because _init is
                                                   # called at the start of
                                                   # draw.

        self._cid = Q.ax.figure.callbacks.connect('dpi_changed',
                                                  on_dpi_change)

        self.labelpos = labelpos
        self.labelcolor = labelcolor
        self.fontproperties = fontproperties or dict()
        self.kw = kw
        _fp = self.fontproperties
        # boxprops = dict(facecolor='red')
        self.text = mtext.Text(
                        text=label,  # bbox=boxprops,
                        horizontalalignment=self.halign[self.labelpos],
                        verticalalignment=self.valign[self.labelpos],
                        fontproperties=font_manager.FontProperties(**_fp))

        if self.labelcolor is not None:
            self.text.set_color(self.labelcolor)
        self._initialized = False
        self.zorder = Q.zorder + 0.1
