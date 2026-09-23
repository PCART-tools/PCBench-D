    def __init__(self, ax, label, initial='',
                 color='.95', hovercolor='1', label_pad=.01):
        """
        Parameters
        ----------
        ax : `~matplotlib.axes.Axes`
            The `~.axes.Axes` instance the button will be placed into.
        label : str
            Label for this text box.
        initial : str
            Initial value in the text box.
        color : color
            The color of the box.
        hovercolor : color
            The color of the box when the mouse is over it.
        label_pad : float
            The distance between the label and the right side of the textbox.
        """
        AxesWidget.__init__(self, ax)

        self.DIST_FROM_LEFT = .05

        self.params_to_disable = [key for key in rcParams if 'keymap' in key]

        self.text = initial
        self.label = ax.text(-label_pad, 0.5, label,
                             verticalalignment='center',
                             horizontalalignment='right',
                             transform=ax.transAxes)
        self.text_disp = self._make_text_disp(self.text)

        self.cnt = 0
        self.change_observers = {}
        self.submit_observers = {}

        # If these lines are removed, the cursor won't appear the first
        # time the box is clicked:
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        self.cursor_index = 0

        # Because this is initialized, _render_cursor
        # can assume that cursor exists.
        self.cursor = self.ax.vlines(0, 0, 0)
        self.cursor.set_visible(False)

        self.connect_event('button_press_event', self._click)
        self.connect_event('button_release_event', self._release)
        self.connect_event('motion_notify_event', self._motion)
        self.connect_event('key_press_event', self._keypress)
        self.connect_event('resize_event', self._resize)
        ax.set_navigate(False)
        ax.set_facecolor(color)
        ax.set_xticks([])
        ax.set_yticks([])
        self.color = color
        self.hovercolor = hovercolor

        self._lastcolor = color

        self.capturekeystrokes = False
