    @_api.make_keyword_only("3.7", name="color")
    def __init__(self, ax, label, initial='',
                 color='.95', hovercolor='1', label_pad=.01,
                 textalignment="left"):
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
        textalignment : {'left', 'center', 'right'}
            The horizontal location of the text.
        """
        super().__init__(ax)

        self._text_position = _api.check_getitem(
            {"left": 0.05, "center": 0.5, "right": 0.95},
            textalignment=textalignment)

        self.label = ax.text(
            -label_pad, 0.5, label, transform=ax.transAxes,
            verticalalignment='center', horizontalalignment='right')

        # TextBox's text object should not parse mathtext at all.
        self.text_disp = self.ax.text(
            self._text_position, 0.5, initial, transform=self.ax.transAxes,
            verticalalignment='center', horizontalalignment=textalignment,
            parse_math=False)

        self._observers = cbook.CallbackRegistry(signals=["change", "submit"])

        ax.set(
            xlim=(0, 1), ylim=(0, 1),  # s.t. cursor appears from first click.
            navigate=False, facecolor=color,
            xticks=[], yticks=[])

        self.cursor_index = 0

        self.cursor = ax.vlines(0, 0, 0, visible=False, color="k", lw=1,
                                transform=mpl.transforms.IdentityTransform())

        self.connect_event('button_press_event', self._click)
        self.connect_event('button_release_event', self._release)
        self.connect_event('motion_notify_event', self._motion)
        self.connect_event('key_press_event', self._keypress)
        self.connect_event('resize_event', self._resize)

        self.color = color
        self.hovercolor = hovercolor

        self.capturekeystrokes = False
