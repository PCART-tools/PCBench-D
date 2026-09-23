    def __init__(self, ax, labels, actives):
        """
        Add check buttons to :class:`matplotlib.axes.Axes` instance *ax*

        *labels*
            A len(buttons) list of labels as strings

        *actives*
            A len(buttons) list of booleans indicating whether
             the button is active
        """
        AxesWidget.__init__(self, ax)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)

        if len(labels) > 1:
            dy = 1. / (len(labels) + 1)
            ys = np.linspace(1 - dy, dy, len(labels))
        else:
            dy = 0.25
            ys = [0.5]

        cnt = 0
        axcolor = ax.get_facecolor()

        self.labels = []
        self.lines = []
        self.rectangles = []

        lineparams = {'color': 'k', 'linewidth': 1.25,
                      'transform': ax.transAxes, 'solid_capstyle': 'butt'}
        for y, label in zip(ys, labels):
            t = ax.text(0.25, y, label, transform=ax.transAxes,
                        horizontalalignment='left',
                        verticalalignment='center')

            w, h = dy / 2., dy / 2.
            x, y = 0.05, y - h / 2.

            p = Rectangle(xy=(x, y), width=w, height=h, edgecolor='black',
                          facecolor=axcolor, transform=ax.transAxes)

            l1 = Line2D([x, x + w], [y + h, y], **lineparams)
            l2 = Line2D([x, x + w], [y, y + h], **lineparams)

            l1.set_visible(actives[cnt])
            l2.set_visible(actives[cnt])
            self.labels.append(t)
            self.rectangles.append(p)
            self.lines.append((l1, l2))
            ax.add_patch(p)
            ax.add_line(l1)
            ax.add_line(l2)
            cnt += 1

        self.connect_event('button_press_event', self._clicked)

        self.cnt = 0
        self.observers = {}
