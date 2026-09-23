class _SelectorWidget(AxesWidget):

    def __init__(self, ax, onselect, useblit=False, button=None,
                 state_modifier_keys=None):
        super().__init__(ax)

        self.visible = True
        self.onselect = onselect
        self.useblit = useblit and self.canvas.supports_blit
        self.connect_default_events()

        self.state_modifier_keys = dict(move=' ', clear='escape',
                                        square='shift', center='control')
        self.state_modifier_keys.update(state_modifier_keys or {})

        self.background = None

        if isinstance(button, Integral):
            self.validButtons = [button]
        else:
            self.validButtons = button

        # Set to True when a selection is completed, otherwise is False
        self._selection_completed = False

        # will save the data (position at mouseclick)
        self._eventpress = None
        # will save the data (pos. at mouserelease)
        self._eventrelease = None
        self._prev_event = None
        self._state = set()
        self._default_state = set()

    eventpress = _api.deprecate_privatize_attribute("3.5")
    eventrelease = _api.deprecate_privatize_attribute("3.5")
    state = _api.deprecate_privatize_attribute("3.5")

    def set_active(self, active):
        super().set_active(active)
        if active:
            self.update_background(None)

    def update_background(self, event):
        """Force an update of the background."""
        # If you add a call to `ignore` here, you'll want to check edge case:
        # `release` can call a draw event even when `ignore` is True.
        if not self.useblit:
            return
        # Make sure that widget artists don't get accidentally included in the
        # background, by re-rendering the background if needed (and then
        # re-re-rendering the canvas with the visible widget artists).
        needs_redraw = any(artist.get_visible() for artist in self.artists)
        with ExitStack() as stack:
            if needs_redraw:
                for artist in self.artists:
                    stack.enter_context(artist._cm_set(visible=False))
                self.canvas.draw()
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        if needs_redraw:
            for artist in self.artists:
                self.ax.draw_artist(artist)

    def connect_default_events(self):
        """Connect the major canvas events to methods."""
        self.connect_event('motion_notify_event', self.onmove)
        self.connect_event('button_press_event', self.press)
        self.connect_event('button_release_event', self.release)
        self.connect_event('draw_event', self.update_background)
        self.connect_event('key_press_event', self.on_key_press)
        self.connect_event('key_release_event', self.on_key_release)
        self.connect_event('scroll_event', self.on_scroll)

    def ignore(self, event):
        # docstring inherited
        if not self.active or not self.ax.get_visible():
            return True
        # If canvas was locked
        if not self.canvas.widgetlock.available(self):
            return True
        if not hasattr(event, 'button'):
            event.button = None
        # Only do rectangle selection if event was triggered
        # with a desired button
        if (self.validButtons is not None
                and event.button not in self.validButtons):
            return True
        # If no button was pressed yet ignore the event if it was out
        # of the axes
        if self._eventpress is None:
            return event.inaxes != self.ax
        # If a button was pressed, check if the release-button is the same.
        if event.button == self._eventpress.button:
            return False
        # If a button was pressed, check if the release-button is the same.
        return (event.inaxes != self.ax or
                event.button != self._eventpress.button)

    def update(self):
        """Draw using blit() or draw_idle(), depending on ``self.useblit``."""
        if not self.ax.get_visible() or self.ax.figure._cachedRenderer is None:
            return False
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            else:
                self.update_background(None)
            for artist in self.artists:
                self.ax.draw_artist(artist)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
        return False

    def _get_data(self, event):
        """Get the xdata and ydata for event, with limits."""
        if event.xdata is None:
            return None, None
        xdata = np.clip(event.xdata, *self.ax.get_xbound())
        ydata = np.clip(event.ydata, *self.ax.get_ybound())
        return xdata, ydata

    def _clean_event(self, event):
        """
        Preprocess an event:

        - Replace *event* by the previous event if *event* has no ``xdata``.
        - Clip ``xdata`` and ``ydata`` to the axes limits.
        - Update the previous event.
        """
        if event.xdata is None:
            event = self._prev_event
        else:
            event = copy.copy(event)
        event.xdata, event.ydata = self._get_data(event)
        self._prev_event = event
        return event

    def press(self, event):
        """Button press handler and validator."""
        if not self.ignore(event):
            event = self._clean_event(event)
            self._eventpress = event
            self._prev_event = event
            key = event.key or ''
            key = key.replace('ctrl', 'control')
            # move state is locked in on a button press
            if key == self.state_modifier_keys['move']:
                self._state.add('move')
            self._press(event)
            return True
        return False

    def _press(self, event):
        """Button press event handler."""

    def release(self, event):
        """Button release event handler and validator."""
        if not self.ignore(event) and self._eventpress:
            event = self._clean_event(event)
            self._eventrelease = event
            self._release(event)
            self._eventpress = None
            self._eventrelease = None
            self._state.discard('move')
            return True
        return False

    def _release(self, event):
        """Button release event handler."""

    def onmove(self, event):
        """Cursor move event handler and validator."""
        if not self.ignore(event) and self._eventpress:
            event = self._clean_event(event)
            self._onmove(event)
            return True
        return False

    def _onmove(self, event):
        """Cursor move event handler."""

    def on_scroll(self, event):
        """Mouse scroll event handler and validator."""
        if not self.ignore(event):
            self._on_scroll(event)

    def _on_scroll(self, event):
        """Mouse scroll event handler."""

    def on_key_press(self, event):
        """Key press event handler and validator for all selection widgets."""
        if self.active:
            key = event.key or ''
            key = key.replace('ctrl', 'control')
            if key == self.state_modifier_keys['clear']:
                self.clear()
                return
            for (state, modifier) in self.state_modifier_keys.items():
                if modifier in key:
                    self._state.add(state)
            self._on_key_press(event)

    def _on_key_press(self, event):
        """Key press event handler - for widget-specific key press actions."""

    def on_key_release(self, event):
        """Key release event handler and validator."""
        if self.active:
            key = event.key or ''
            for (state, modifier) in self.state_modifier_keys.items():
                if modifier in key:
                    self._state.discard(state)
            self._on_key_release(event)

    def _on_key_release(self, event):
        """Key release event handler."""

    def set_visible(self, visible):
        """Set the visibility of our artists."""
        self.visible = visible
        for artist in self.artists:
            artist.set_visible(visible)

    def clear(self):
        """Clear the selection and set the selector ready to make a new one."""
        self._selection_completed = False
        self.set_visible(False)
        self.update()

    @property
    def artists(self):
        """Tuple of the artists of the selector."""
        handles_artists = getattr(self, '_handles_artists', ())
        return (self._selection_artist,) + handles_artists

    def set_props(self, **props):
        """
        Set the properties of the selector artist. See the `props` argument
        in the selector docstring to know which properties are supported.
        """
        artist = self._selection_artist
        props = cbook.normalize_kwargs(props, artist)
        artist.set(**props)
        if self.useblit:
            self.update()
        self._props.update(props)

    def set_handle_props(self, **handle_props):
        """
        Set the properties of the handles selector artist. See the
        `handle_props` argument in the selector docstring to know which
        properties are supported.
        """
        if not hasattr(self, '_handles_artists'):
            raise NotImplementedError("This selector doesn't have handles.")

        artist = self._handles_artists[0]
        handle_props = cbook.normalize_kwargs(handle_props, artist)
        for handle in self._handles_artists:
            handle.set(**handle_props)
        if self.useblit:
            self.update()
        self._handle_props.update(handle_props)
