    def __init__(self, targetfig, toolfig):
        """
        Parameters
        ----------
        targetfig : `.Figure`
            The figure instance to adjust.
        toolfig : `.Figure`
            The figure instance to embed the subplot tool into.
        """

        self.targetfig = targetfig
        toolfig.subplots_adjust(left=0.2, right=0.9)

        self.axleft = toolfig.add_subplot(711)
        self.axleft.set_title('Click on slider to adjust subplot param')
        self.axleft.set_navigate(False)

        self.sliderleft = Slider(self.axleft, 'left',
                                 0, 1, targetfig.subplotpars.left,
                                 closedmax=False)
        self.sliderleft.on_changed(self.funcleft)

        self.axbottom = toolfig.add_subplot(712)
        self.axbottom.set_navigate(False)
        self.sliderbottom = Slider(self.axbottom,
                                   'bottom', 0, 1,
                                   targetfig.subplotpars.bottom,
                                   closedmax=False)
        self.sliderbottom.on_changed(self.funcbottom)

        self.axright = toolfig.add_subplot(713)
        self.axright.set_navigate(False)
        self.sliderright = Slider(self.axright, 'right', 0, 1,
                                  targetfig.subplotpars.right,
                                  closedmin=False)
        self.sliderright.on_changed(self.funcright)

        self.axtop = toolfig.add_subplot(714)
        self.axtop.set_navigate(False)
        self.slidertop = Slider(self.axtop, 'top', 0, 1,
                                targetfig.subplotpars.top,
                                closedmin=False)
        self.slidertop.on_changed(self.functop)

        self.axwspace = toolfig.add_subplot(715)
        self.axwspace.set_navigate(False)
        self.sliderwspace = Slider(self.axwspace, 'wspace',
                                   0, 1, targetfig.subplotpars.wspace,
                                   closedmax=False)
        self.sliderwspace.on_changed(self.funcwspace)

        self.axhspace = toolfig.add_subplot(716)
        self.axhspace.set_navigate(False)
        self.sliderhspace = Slider(self.axhspace, 'hspace',
                                   0, 1, targetfig.subplotpars.hspace,
                                   closedmax=False)
        self.sliderhspace.on_changed(self.funchspace)

        # constraints
        self.sliderleft.slidermax = self.sliderright
        self.sliderright.slidermin = self.sliderleft
        self.sliderbottom.slidermax = self.slidertop
        self.slidertop.slidermin = self.sliderbottom

        bax = toolfig.add_axes([0.8, 0.05, 0.15, 0.075])
        self.buttonreset = Button(bax, 'Reset')

        sliders = (self.sliderleft, self.sliderbottom, self.sliderright,
                   self.slidertop, self.sliderwspace, self.sliderhspace,)

        def func(event):
            with ExitStack() as stack:
                # Temporarily disable drawing on self and self's sliders.
                stack.enter_context(cbook._setattr_cm(self, drawon=False))
                for slider in sliders:
                    stack.enter_context(
                        cbook._setattr_cm(slider, drawon=False))
                # Reset the slider to the initial position.
                for slider in sliders:
                    slider.reset()
            # Draw the canvas.
            if self.drawon:
                toolfig.canvas.draw()
                self.targetfig.canvas.draw()

        # during reset there can be a temporary invalid state
        # depending on the order of the reset so we turn off
        # validation for the resetting
        validate = toolfig.subplotpars.validate
        toolfig.subplotpars.validate = False
        self.buttonreset.on_clicked(func)
        toolfig.subplotpars.validate = validate
