    def __init__(self, ax, labels, actives=None, *, useblit=True,
                 label_props=None, frame_props=None, check_props=None):
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
        useblit : bool, default: True
            Use blitting for faster drawing if supported by the backend.
            See the tutorial :doc:`/tutorials/advanced/blitting` for details.
        label_props : dict, optional
            Dictionary of `.Text` properties to be used for the labels.

            .. versionadded:: 3.7
        frame_props : dict, optional
            Dictionary of scatter `.Collection` properties to be used for the
            check button frame. Defaults (label font size / 2)**2 size, black
            edgecolor, no facecolor, and 1.0 linewidth.

            .. versionadded:: 3.7
        check_props : dict, optional
            Dictionary of scatter `.Collection` properties to be used for the
            check button check. Defaults to (label font size / 2)**2 size,
            black color, and 1.0 linewidth.

            .. versionadded:: 3.7
        """
        super().__init__(ax)

        _api.check_isinstance((dict, None), label_props=label_props,
                              frame_props=frame_props, check_props=check_props)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)

        if actives is None:
            actives = [False] * len(labels)

        self._useblit = useblit and self.canvas.supports_blit
        self._background = None

        ys = np.linspace(1, 0, len(labels)+2)[1:-1]

        label_props = _expand_text_props(label_props)
        self.labels = [
            ax.text(0.25, y, label, transform=ax.transAxes,
                    horizontalalignment="left", verticalalignment="center",
                    **props)
            for y, label, props in zip(ys, labels, label_props)]
        text_size = np.array([text.get_fontsize() for text in self.labels]) / 2

        frame_props = {
            's': text_size**2,
            'linewidth': 1,
            **cbook.normalize_kwargs(frame_props, collections.PathCollection),
            'marker': 's',
            'transform': ax.transAxes,
        }
        frame_props.setdefault('facecolor', frame_props.get('color', 'none'))
        frame_props.setdefault('edgecolor', frame_props.pop('color', 'black'))
        self._frames = ax.scatter([0.15] * len(ys), ys, **frame_props)
        check_props = {
            'linewidth': 1,
            's': text_size**2,
            **cbook.normalize_kwargs(check_props, collections.PathCollection),
            'marker': 'x',
            'transform': ax.transAxes,
            'animated': self._useblit,
        }
        check_props.setdefault('facecolor', check_props.pop('color', 'black'))
        self._checks = ax.scatter([0.15] * len(ys), ys, **check_props)
        # The user may have passed custom colours in check_props, so we need to
        # create the checks (above), and modify the visibility after getting
        # whatever the user set.
        self._init_status(actives)

        self.connect_event('button_press_event', self._clicked)
        if self._useblit:
            self.connect_event('draw_event', self._clear)

        self._observers = cbook.CallbackRegistry(signals=["clicked"])
