    def __init__(self, ax, orientation, closedmin, closedmax,
                 valmin, valmax, valfmt, dragging, valstep):
        if ax.name == '3d':
            raise ValueError('Sliders cannot be added to 3D Axes')

        super().__init__(ax)
        _api.check_in_list(['horizontal', 'vertical'], orientation=orientation)

        self.orientation = orientation
        self.closedmin = closedmin
        self.closedmax = closedmax
        self.valmin = valmin
        self.valmax = valmax
        self.valstep = valstep
        self.drag_active = False
        self.valfmt = valfmt

        if orientation == "vertical":
            ax.set_ylim((valmin, valmax))
            axis = ax.yaxis
        else:
            ax.set_xlim((valmin, valmax))
            axis = ax.xaxis

        self._fmt = axis.get_major_formatter()
        if not isinstance(self._fmt, ticker.ScalarFormatter):
            self._fmt = ticker.ScalarFormatter()
            self._fmt.set_axis(axis)
        self._fmt.set_useOffset(False)  # No additive offset.
        self._fmt.set_useMathText(True)  # x sign before multiplicative offset.

        ax.set_axis_off()
        ax.set_navigate(False)

        self.connect_event("button_press_event", self._update)
        self.connect_event("button_release_event", self._update)
        if dragging:
            self.connect_event("motion_notify_event", self._update)
        self._observers = cbook.CallbackRegistry()
