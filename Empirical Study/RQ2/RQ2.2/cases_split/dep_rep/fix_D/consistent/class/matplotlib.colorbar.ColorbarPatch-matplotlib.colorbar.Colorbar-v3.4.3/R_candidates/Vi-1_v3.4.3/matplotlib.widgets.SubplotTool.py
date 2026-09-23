class SubplotTool(Widget):
    """
    A tool to adjust the subplot params of a `matplotlib.figure.Figure`.
    """

    def __init__(self, targetfig, toolfig):
        """
        Parameters
        ----------
        targetfig : `.Figure`
            The figure instance to adjust.
        toolfig : `.Figure`
            The figure instance to embed the subplot tool into.
        """

        self.figure = toolfig
        self.targetfig = targetfig
        toolfig.subplots_adjust(left=0.2, right=0.9)
        toolfig.suptitle("Click on slider to adjust subplot param")

        self._sliders = []
        names = ["left", "bottom", "right", "top", "wspace", "hspace"]
        # The last subplot, removed below, keeps space for the "Reset" button.
        for name, ax in zip(names, toolfig.subplots(len(names) + 1)):
            ax.set_navigate(False)
            slider = Slider(ax, name,
                            0, 1, getattr(targetfig.subplotpars, name))
            slider.on_changed(self._on_slider_changed)
            self._sliders.append(slider)
        toolfig.axes[-1].remove()
        (self.sliderleft, self.sliderbottom, self.sliderright, self.slidertop,
         self.sliderwspace, self.sliderhspace) = self._sliders
        for slider in [self.sliderleft, self.sliderbottom,
                       self.sliderwspace, self.sliderhspace]:
            slider.closedmax = False
        for slider in [self.sliderright, self.slidertop]:
            slider.closedmin = False

        # constraints
        self.sliderleft.slidermax = self.sliderright
        self.sliderright.slidermin = self.sliderleft
        self.sliderbottom.slidermax = self.slidertop
        self.slidertop.slidermin = self.sliderbottom

        bax = toolfig.add_axes([0.8, 0.05, 0.15, 0.075])
        self.buttonreset = Button(bax, 'Reset')

        # During reset there can be a temporary invalid state depending on the
        # order of the reset so we turn off validation for the resetting
        with cbook._setattr_cm(toolfig.subplotpars, validate=False):
            self.buttonreset.on_clicked(self._on_reset)

    def _on_slider_changed(self, _):
        self.targetfig.subplots_adjust(
            **{slider.label.get_text(): slider.val
               for slider in self._sliders})
        if self.drawon:
            self.targetfig.canvas.draw()

    def _on_reset(self, event):
        with ExitStack() as stack:
            # Temporarily disable drawing on self and self's sliders.
            stack.enter_context(cbook._setattr_cm(self, drawon=False))
            for slider in self._sliders:
                stack.enter_context(cbook._setattr_cm(slider, drawon=False))
            # Reset the slider to the initial position.
            for slider in self._sliders:
                slider.reset()
        # Draw the canvas.
        if self.drawon:
            event.canvas.draw()
            self.targetfig.canvas.draw()

    axleft = _api.deprecated("3.3")(
        property(lambda self: self.sliderleft.ax))
    axright = _api.deprecated("3.3")(
        property(lambda self: self.sliderright.ax))
    axbottom = _api.deprecated("3.3")(
        property(lambda self: self.sliderbottom.ax))
    axtop = _api.deprecated("3.3")(
        property(lambda self: self.slidertop.ax))
    axwspace = _api.deprecated("3.3")(
        property(lambda self: self.sliderwspace.ax))
    axhspace = _api.deprecated("3.3")(
        property(lambda self: self.sliderhspace.ax))

    @_api.deprecated("3.3")
    def funcleft(self, val):
        self.targetfig.subplots_adjust(left=val)
        if self.drawon:
            self.targetfig.canvas.draw()

    @_api.deprecated("3.3")
    def funcright(self, val):
        self.targetfig.subplots_adjust(right=val)
        if self.drawon:
            self.targetfig.canvas.draw()

    @_api.deprecated("3.3")
    def funcbottom(self, val):
        self.targetfig.subplots_adjust(bottom=val)
        if self.drawon:
            self.targetfig.canvas.draw()

    @_api.deprecated("3.3")
    def functop(self, val):
        self.targetfig.subplots_adjust(top=val)
        if self.drawon:
            self.targetfig.canvas.draw()

    @_api.deprecated("3.3")
    def funcwspace(self, val):
        self.targetfig.subplots_adjust(wspace=val)
        if self.drawon:
            self.targetfig.canvas.draw()

    @_api.deprecated("3.3")
    def funchspace(self, val):
        self.targetfig.subplots_adjust(hspace=val)
        if self.drawon:
            self.targetfig.canvas.draw()
