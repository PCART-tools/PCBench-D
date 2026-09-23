    def __init__(self, ax, labels, active=0, activecolor='blue'):
        """
        Add radio buttons to an `~.axes.Axes`.

        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The Axes to add the buttons to.
        labels : list of str
            The button labels.
        active : int
            The index of the initially selected button.
        activecolor : color
            The color of the selected button.
        """
        super().__init__(ax)
        self.activecolor = activecolor
        self.value_selected = None

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)
        dy = 1. / (len(labels) + 1)
        ys = np.linspace(1 - dy, dy, len(labels))
        cnt = 0
        axcolor = ax.get_facecolor()

        # scale the radius of the circle with the spacing between each one
        circle_radius = dy / 2 - 0.01
        # default to hard-coded value if the radius becomes too large
        circle_radius = min(circle_radius, 0.05)

        self.labels = []
        self.circles = []
        for y, label in zip(ys, labels):
            t = ax.text(0.25, y, label, transform=ax.transAxes,
                        horizontalalignment='left',
                        verticalalignment='center')

            if cnt == active:
                self.value_selected = label
                facecolor = activecolor
            else:
                facecolor = axcolor

            p = Circle(xy=(0.15, y), radius=circle_radius, edgecolor='black',
                       facecolor=facecolor, transform=ax.transAxes)

            self.labels.append(t)
            self.circles.append(p)
            ax.add_patch(p)
            cnt += 1

        self.connect_event('button_press_event', self._clicked)

        self._observers = cbook.CallbackRegistry(signals=["clicked"])
