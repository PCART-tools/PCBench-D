    def __init__(self, ax, label, valmin, valmax, valinit=0.5, valfmt='%1.2f',
                 closedmin=True, closedmax=True, slidermin=None,
                 slidermax=None, dragging=True, valstep=None,
                 orientation='horizontal', **kwargs):
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

        valinit : float, optional, default: 0.5
            The slider initial position.

        valfmt : str, optional, default: "%1.2f"
            Used to format the slider value, fprint format string.

        closedmin : bool, optional, default: True
            Whether the slider interval is closed on the bottom.

        closedmax : bool, optional, default: True
            Whether the slider interval is closed on the top.

        slidermin : Slider, optional, default: None
            Do not allow the current slider to have a value less than
            the value of the Slider `slidermin`.

        slidermax : Slider, optional, default: None
            Do not allow the current slider to have a value greater than
            the value of the Slider `slidermax`.

        dragging : bool, optional, default: True
            If True the slider can be dragged by the mouse.

        valstep : float, optional, default: None
            If given, the slider will snap to multiples of `valstep`.

        orientation : {'horizontal', 'vertical'}, default: 'horizontal'
            The orientation of the slider.

        Notes
        -----
        Additional kwargs are passed on to ``self.poly`` which is the
        `~matplotlib.patches.Rectangle` that draws the slider knob.  See the
        `.Rectangle` documentation for valid property names (``facecolor``,
        ``edgecolor``, ``alpha``, etc.).
        """
        if ax.name == '3d':
            raise ValueError('Sliders cannot be added to 3D Axes')

        AxesWidget.__init__(self, ax)

        if slidermin is not None and not hasattr(slidermin, 'val'):
            raise ValueError("Argument slidermin ({}) has no 'val'"
                             .format(type(slidermin)))
        if slidermax is not None and not hasattr(slidermax, 'val'):
            raise ValueError("Argument slidermax ({}) has no 'val'"
                             .format(type(slidermax)))
        if orientation not in ['horizontal', 'vertical']:
            raise ValueError("Argument orientation ({}) must be either"
                             "'horizontal' or 'vertical'".format(orientation))

        self.orientation = orientation
        self.closedmin = closedmin
        self.closedmax = closedmax
        self.slidermin = slidermin
        self.slidermax = slidermax
        self.drag_active = False
        self.valmin = valmin
        self.valmax = valmax
        self.valstep = valstep
        valinit = self._value_in_bounds(valinit)
        if valinit is None:
            valinit = valmin
        self.val = valinit
        self.valinit = valinit
        if orientation == 'vertical':
            self.poly = ax.axhspan(valmin, valinit, 0, 1, **kwargs)
            self.hline = ax.axhline(valinit, 0, 1, color='r', lw=1)
        else:
            self.poly = ax.axvspan(valmin, valinit, 0, 1, **kwargs)
            self.vline = ax.axvline(valinit, 0, 1, color='r', lw=1)

        self.valfmt = valfmt
        ax.set_yticks([])
        if orientation == 'vertical':
            ax.set_ylim((valmin, valmax))
        else:
            ax.set_xlim((valmin, valmax))
        ax.set_xticks([])
        ax.set_navigate(False)

        self.connect_event('button_press_event', self._update)
        self.connect_event('button_release_event', self._update)
        if dragging:
            self.connect_event('motion_notify_event', self._update)
        if orientation == 'vertical':
            self.label = ax.text(0.5, 1.02, label, transform=ax.transAxes,
                                 verticalalignment='bottom',
                                 horizontalalignment='center')

            self.valtext = ax.text(0.5, -0.02, valfmt % valinit,
                                   transform=ax.transAxes,
                                   verticalalignment='top',
                                   horizontalalignment='center')
        else:
            self.label = ax.text(-0.02, 0.5, label, transform=ax.transAxes,
                                 verticalalignment='center',
                                 horizontalalignment='right')

            self.valtext = ax.text(1.02, 0.5, valfmt % valinit,
                                   transform=ax.transAxes,
                                   verticalalignment='center',
                                   horizontalalignment='left')

        self.cnt = 0
        self.observers = {}

        self.set_val(valinit)
