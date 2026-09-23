    def __init__(self, ax, labels, actives=None):
        """
        Add check buttons to `matplotlib.axes.Axes` instance *ax*.

        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The parent Axes for the widget.

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

        self._observers = cbook.CallbackRegistry(signals=["clicked"])
