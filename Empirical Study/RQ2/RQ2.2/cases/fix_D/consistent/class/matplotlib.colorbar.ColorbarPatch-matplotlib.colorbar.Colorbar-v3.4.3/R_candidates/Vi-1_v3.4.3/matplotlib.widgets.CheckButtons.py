class CheckButtons(AxesWidget):
    r"""
    A GUI neutral set of check buttons.

    For the check buttons to remain responsive you must keep a
    reference to this object.

    Connect to the CheckButtons with the `.on_clicked` method.

    Attributes
    ----------
    ax : `~matplotlib.axes.Axes`
        The parent axes for the widget.
    labels : list of `.Text`

    rectangles : list of `.Rectangle`

    lines : list of (`.Line2D`, `.Line2D`) pairs
        List of lines for the x's in the check boxes.  These lines exist for
        each box, but have ``set_visible(False)`` when its box is not checked.
    """

    cnt = _api.deprecated("3.4")(property(  # Not real, but close enough.
        lambda self: len(self._observers.callbacks['clicked'])))
    observers = _api.deprecated("3.4")(property(
        lambda self: self._observers.callbacks['clicked']))

    def __init__(self, ax, labels, actives=None):
        """
        Add check buttons to `matplotlib.axes.Axes` instance *ax*.

        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The parent axes for the widget.

        labels : list of str
            The labels of the check buttons.

        actives : list of bool, optional
            The initial check states of the buttons. The list must have the
            same length as *labels*. If not given, all buttons are unchecked.
        """
        super().__init__(ax)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)

        if actives is None:
            actives = [False] * len(labels)

        if len(labels) > 1:
            dy = 1. / (len(labels) + 1)
            ys = np.linspace(1 - dy, dy, len(labels))
        else:
            dy = 0.25
            ys = [0.5]

        axcolor = ax.get_facecolor()

        self.labels = []
        self.lines = []
        self.rectangles = []

        lineparams = {'color': 'k', 'linewidth': 1.25,
                      'transform': ax.transAxes, 'solid_capstyle': 'butt'}
        for y, label, active in zip(ys, labels, actives):
            t = ax.text(0.25, y, label, transform=ax.transAxes,
                        horizontalalignment='left',
                        verticalalignment='center')

            w, h = dy / 2, dy / 2
            x, y = 0.05, y - h / 2

            p = Rectangle(xy=(x, y), width=w, height=h, edgecolor='black',
                          facecolor=axcolor, transform=ax.transAxes)

            l1 = Line2D([x, x + w], [y + h, y], **lineparams)
            l2 = Line2D([x, x + w], [y, y + h], **lineparams)

            l1.set_visible(active)
            l2.set_visible(active)
            self.labels.append(t)
            self.rectangles.append(p)
            self.lines.append((l1, l2))
            ax.add_patch(p)
            ax.add_line(l1)
            ax.add_line(l2)

        self.connect_event('button_press_event', self._clicked)

        self._observers = cbook.CallbackRegistry()

    def _clicked(self, event):
        if self.ignore(event) or event.button != 1 or event.inaxes != self.ax:
            return
        for i, (p, t) in enumerate(zip(self.rectangles, self.labels)):
            if (t.get_window_extent().contains(event.x, event.y) or
                    p.get_window_extent().contains(event.x, event.y)):
                self.set_active(i)
                break

    def set_active(self, index):
        """
        Toggle (activate or deactivate) a check button by index.

        Callbacks will be triggered if :attr:`eventson` is True.

        Parameters
        ----------
        index : int
            Index of the check button to toggle.

        Raises
        ------
        ValueError
            If *index* is invalid.
        """
        if index not in range(len(self.labels)):
            raise ValueError(f'Invalid CheckButton index: {index}')

        l1, l2 = self.lines[index]
        l1.set_visible(not l1.get_visible())
        l2.set_visible(not l2.get_visible())

        if self.drawon:
            self.ax.figure.canvas.draw()

        if self.eventson:
            self._observers.process('clicked', self.labels[index].get_text())

    def get_status(self):
        """
        Return a tuple of the status (True/False) of all of the check buttons.
        """
        return [l1.get_visible() for (l1, l2) in self.lines]

    def on_clicked(self, func):
        """
        Connect the callback function *func* to button click events.

        Returns a connection id, which can be used to disconnect the callback.
        """
        return self._observers.connect('clicked', lambda text: func(text))

    def disconnect(self, cid):
        """Remove the observer with connection id *cid*."""
        self._observers.disconnect(cid)
