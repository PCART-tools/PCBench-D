    def __init__(self, ax, label, image=None,
                 color='0.85', hovercolor='0.95'):
        """
        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance the button will be placed into.

        label : str
            The button text. Accepts string.

        image : array, mpl image, Pillow Image
            The image to place in the button, if not *None*.
            Can be any legal arg to imshow (numpy array,
            matplotlib Image instance, or Pillow Image).

        color : color
            The color of the button when not activated.

        hovercolor : color
            The color of the button when the mouse is over it.
        """
        AxesWidget.__init__(self, ax)

        if image is not None:
            ax.imshow(image)
        self.label = ax.text(0.5, 0.5, label,
                             verticalalignment='center',
                             horizontalalignment='center',
                             transform=ax.transAxes)

        self.cnt = 0
        self.observers = {}

        self.connect_event('button_press_event', self._click)
        self.connect_event('button_release_event', self._release)
        self.connect_event('motion_notify_event', self._motion)
        ax.set_navigate(False)
        ax.set_facecolor(color)
        ax.set_xticks([])
        ax.set_yticks([])
        self.color = color
        self.hovercolor = hovercolor

        self._lastcolor = color
