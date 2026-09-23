    def __init__(self, ax, label, valmin, valmax, valinit=0.5, valfmt=None,
                 closedmin=True, closedmax=True, slidermin=None,
                 slidermax=None, dragging=True, valstep=None,
                 orientation='horizontal', *, initcolor='r', **kwargs):
        """
        Parameters
        ----------
        ax : Axes
            The Axes to put the slider in.

        label : str
            Slider label.

        valmin : float
            The minimum value of the slider.

        valmax : float
            The maximum value of the slider.

        valinit : float, default: 0.5
            The slider initial position.

        valfmt : str, default: None
            %-format string used to format the slider value.  If None, a
            `.ScalarFormatter` is used instead.

        closedmin : bool, default: True
            Whether the slider interval is closed on the bottom.

        closedmax : bool, default: True
            Whether the slider interval is closed on the top.

        slidermin : Slider, default: None
            Do not allow the current slider to have a value less than
            the value of the Slider *slidermin*.

        slidermax : Slider, default: None
            Do not allow the current slider to have a value greater than
            the value of the Slider *slidermax*.

        dragging : bool, default: True
            If True the slider can be dragged by the mouse.

        valstep : float or array-like, default: None
            If a float, the slider will snap to multiples of *valstep*.
            If an array the slider will snap to the values in the array.

        orientation : {'horizontal', 'vertical'}, default: 'horizontal'
            The orientation of the slider.

        initcolor : color, default: 'r'
            The color of the line at the *valinit* position. Set to ``'none'``
            for no line.

        Notes
        -----
        Additional kwargs are passed on to ``self.poly`` which is the
        `~matplotlib.patches.Rectangle` that draws the slider knob.  See the
        `.Rectangle` documentation for valid property names (``facecolor``,
        ``edgecolor``, ``alpha``, etc.).
        """
        super().__init__(ax, orientation, closedmin, closedmax,
                         valmin, valmax, valfmt, dragging, valstep)

        if slidermin is not None and not hasattr(slidermin, 'val'):
            raise ValueError(
                f"Argument slidermin ({type(slidermin)}) has no 'val'")
        if slidermax is not None and not hasattr(slidermax, 'val'):
            raise ValueError(
                f"Argument slidermax ({type(slidermax)}) has no 'val'")
        self.slidermin = slidermin
        self.slidermax = slidermax
        valinit = self._value_in_bounds(valinit)
        if valinit is None:
            valinit = valmin
        self.val = valinit
        self.valinit = valinit
        if orientation == 'vertical':
            self.poly = ax.axhspan(valmin, valinit, 0, 1, **kwargs)
            self.hline = ax.axhline(valinit, 0, 1, color=initcolor, lw=1)
        else:
            self.poly = ax.axvspan(valmin, valinit, 0, 1, **kwargs)
            self.vline = ax.axvline(valinit, 0, 1, color=initcolor, lw=1)

        if orientation == 'vertical':
            self.label = ax.text(0.5, 1.02, label, transform=ax.transAxes,
                                 verticalalignment='bottom',
                                 horizontalalignment='center')

            self.valtext = ax.text(0.5, -0.02, self._format(valinit),
                                   transform=ax.transAxes,
                                   verticalalignment='top',
                                   horizontalalignment='center')
        else:
            self.label = ax.text(-0.02, 0.5, label, transform=ax.transAxes,
                                 verticalalignment='center',
                                 horizontalalignment='right')

            self.valtext = ax.text(1.02, 0.5, self._format(valinit),
                                   transform=ax.transAxes,
                                   verticalalignment='center',
                                   horizontalalignment='left')

        self.set_val(valinit)
