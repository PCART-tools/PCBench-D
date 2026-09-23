class Button(AxesWidget):
    """
    A GUI neutral button.

    For the button to remain responsive you must keep a reference to it.
    Call `.on_clicked` to connect to the button.

    Attributes
    ----------
    ax
        The `matplotlib.axes.Axes` the button renders into.
    label
        A `matplotlib.text.Text` instance.
    color
        The color of the button when not hovering.
    hovercolor
        The color of the button when hovering.
    """

    cnt = _api.deprecated("3.4")(property(  # Not real, but close enough.
        lambda self: len(self._observers.callbacks['clicked'])))
    observers = _api.deprecated("3.4")(property(
        lambda self: self._observers.callbacks['clicked']))

    def __init__(self, ax, label, image=None,
                 color='0.85', hovercolor='0.95'):
        """
        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance the button will be placed into.
        label : str
            The button text.
        image : array-like or PIL Image
            The image to place in the button, if not *None*.  The parameter is
            directly forwarded to `~matplotlib.axes.Axes.imshow`.
        color : color
            The color of the button when not activated.
        hovercolor : color
            The color of the button when the mouse is over it.
        """
        super().__init__(ax)

        if image is not None:
            ax.imshow(image)
        self.label = ax.text(0.5, 0.5, label,
                             verticalalignment='center',
                             horizontalalignment='center',
                             transform=ax.transAxes)

        self._observers = cbook.CallbackRegistry()

        self.connect_event('button_press_event', self._click)
        self.connect_event('button_release_event', self._release)
        self.connect_event('motion_notify_event', self._motion)
        ax.set_navigate(False)
        ax.set_facecolor(color)
        ax.set_xticks([])
        ax.set_yticks([])
        self.color = color
        self.hovercolor = hovercolor

    def _click(self, event):
        if self.ignore(event) or event.inaxes != self.ax or not self.eventson:
            return
        if event.canvas.mouse_grabber != self.ax:
            event.canvas.grab_mouse(self.ax)

    def _release(self, event):
        if self.ignore(event) or event.canvas.mouse_grabber != self.ax:
            return
        event.canvas.release_mouse(self.ax)
        if self.eventson and event.inaxes == self.ax:
            self._observers.process('clicked', event)

    def _motion(self, event):
        if self.ignore(event):
            return
        c = self.hovercolor if event.inaxes == self.ax else self.color
        if not colors.same_color(c, self.ax.get_facecolor()):
            self.ax.set_facecolor(c)
            if self.drawon:
                self.ax.figure.canvas.draw()

    def on_clicked(self, func):
        """
        Connect the callback function *func* to button click events.

        Returns a connection id, which can be used to disconnect the callback.
        """
        return self._observers.connect('clicked', lambda event: func(event))

    def disconnect(self, cid):
        """Remove the callback function with connection id *cid*."""
        self._observers.disconnect(cid)
