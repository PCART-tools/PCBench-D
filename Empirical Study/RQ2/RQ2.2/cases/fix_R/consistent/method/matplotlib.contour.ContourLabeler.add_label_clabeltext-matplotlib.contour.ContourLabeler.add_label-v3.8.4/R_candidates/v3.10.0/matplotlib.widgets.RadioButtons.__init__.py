    def __init__(self, ax, labels, active=0, activecolor=None, *,
                 useblit=True, label_props=None, radio_props=None):
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
        activecolor : :mpltype:`color`
            The color of the selected button. The default is ``'blue'`` if not
            specified here or in *radio_props*.
        useblit : bool, default: True
            Use blitting for faster drawing if supported by the backend.
            See the tutorial :ref:`blitting` for details.

            .. versionadded:: 3.7

        label_props : dict or list of dict, optional
            Dictionary of `.Text` properties to be used for the labels.

            .. versionadded:: 3.7
        radio_props : dict, optional
            Dictionary of scatter `.Collection` properties to be used for the
            radio buttons. Defaults to (label font size / 2)**2 size, black
            edgecolor, and *activecolor* facecolor (when active).

            .. note::
                If a facecolor is supplied in *radio_props*, it will override
                *activecolor*. This may be used to provide an active color per
                button.

            .. versionadded:: 3.7
        """
        super().__init__(ax)

        _api.check_isinstance((dict, None), label_props=label_props,
                              radio_props=radio_props)

        radio_props = cbook.normalize_kwargs(radio_props,
                                             collections.PathCollection)
        if activecolor is not None:
            if 'facecolor' in radio_props:
                _api.warn_external(
                    'Both the *activecolor* parameter and the *facecolor* '
                    'key in the *radio_props* parameter has been specified. '
                    '*activecolor* will be ignored.')
        else:
            activecolor = 'blue'  # Default.

        self._activecolor = activecolor
        self._initial_active = active
        self.value_selected = labels[active]
        self.index_selected = active

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)

        ys = np.linspace(1, 0, len(labels) + 2)[1:-1]

        self._useblit = useblit and self.canvas.supports_blit
        self._background = None

        label_props = _expand_text_props(label_props)
        self.labels = [
            ax.text(0.25, y, label, transform=ax.transAxes,
                    horizontalalignment="left", verticalalignment="center",
                    **props)
            for y, label, props in zip(ys, labels, label_props)]
        text_size = np.array([text.get_fontsize() for text in self.labels]) / 2

        radio_props = {
            's': text_size**2,
            **radio_props,
            'marker': 'o',
            'transform': ax.transAxes,
            'animated': self._useblit,
        }
        radio_props.setdefault('edgecolor', radio_props.get('color', 'black'))
        radio_props.setdefault('facecolor',
                               radio_props.pop('color', activecolor))
        self._buttons = ax.scatter([.15] * len(ys), ys, **radio_props)
        # The user may have passed custom colours in radio_props, so we need to
        # create the radios, and modify the visibility after getting whatever
        # the user set.
        self._active_colors = self._buttons.get_facecolor()
        if len(self._active_colors) == 1:
            self._active_colors = np.repeat(self._active_colors, len(labels),
                                            axis=0)
        self._buttons.set_facecolor(
            [activecolor if i == active else "none"
             for i, activecolor in enumerate(self._active_colors)])

        self.connect_event('button_press_event', self._clicked)
        if self._useblit:
            self.connect_event('draw_event', self._clear)

        self._observers = cbook.CallbackRegistry(signals=["clicked"])
