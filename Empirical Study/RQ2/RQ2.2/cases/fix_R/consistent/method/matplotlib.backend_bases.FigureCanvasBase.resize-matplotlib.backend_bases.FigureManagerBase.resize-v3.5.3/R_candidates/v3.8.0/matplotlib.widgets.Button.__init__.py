    def __init__(self, ax, label, image=None,
                 color='0.85', hovercolor='0.95', *, useblit=True):
        """
        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance the button will be placed into.
        label : str
            The button text.
        image : array-like or PIL Image
            The image to place in the button, if not *None*.  The parameter is
            directly forwarded to `~.axes.Axes.imshow`.
        color : color
            The color of the button when not activated.
        hovercolor : color
            The color of the button when the mouse is over it.
        useblit : bool, default: True
            Use blitting for faster drawing if supported by the backend.
            See the tutorial :ref:`blitting` for details.

            .. versionadded:: 3.7
        """
        super().__init__(ax)

        if image is not None:
            ax.imshow(image)
        self.label = ax.text(0.5, 0.5, label,
                             verticalalignment='center',
                             horizontalalignment='center',
                             transform=ax.transAxes)

        self._useblit = useblit and self.canvas.supports_blit

        self._observers = cbook.CallbackRegistry(signals=["clicked"])

        self.connect_event('button_press_event', self._click)
        self.connect_event('button_release_event', self._release)
        self.connect_event('motion_notify_event', self._motion)
        ax.set_navigate(False)
        ax.set_facecolor(color)
        ax.set_xticks([])
        ax.set_yticks([])
        self.color = color
        self.hovercolor = hovercolor
