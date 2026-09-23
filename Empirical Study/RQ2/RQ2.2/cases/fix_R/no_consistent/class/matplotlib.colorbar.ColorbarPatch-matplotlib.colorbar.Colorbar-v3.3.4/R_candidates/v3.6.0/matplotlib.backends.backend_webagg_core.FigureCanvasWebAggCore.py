class FigureCanvasWebAggCore(backend_agg.FigureCanvasAgg):
    manager_class = _api.classproperty(lambda cls: FigureManagerWebAgg)
    _timer_cls = TimerAsyncio
    # Webagg and friends having the right methods, but still
    # having bugs in practice.  Do not advertise that it works until
    # we can debug this.
    supports_blit = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set to True when the renderer contains data that is newer
        # than the PNG buffer.
        self._png_is_old = True
        # Set to True by the `refresh` message so that the next frame
        # sent to the clients will be a full frame.
        self._force_full = True
        # The last buffer, for diff mode.
        self._last_buff = np.empty((0, 0))
        # Store the current image mode so that at any point, clients can
        # request the information. This should be changed by calling
        # self.set_image_mode(mode) so that the notification can be given
        # to the connected clients.
        self._current_image_mode = 'full'
        # Track mouse events to fill in the x, y position of key events.
        self._last_mouse_xy = (None, None)

    def show(self):
        # show the figure window
        from matplotlib.pyplot import show
        show()

    def draw(self):
        self._png_is_old = True
        try:
            super().draw()
        finally:
            self.manager.refresh_all()  # Swap the frames.

    def blit(self, bbox=None):
        self._png_is_old = True
        self.manager.refresh_all()

    def draw_idle(self):
        self.send_event("draw")

    def set_cursor(self, cursor):
        # docstring inherited
        cursor = _api.check_getitem({
            backend_tools.Cursors.HAND: 'pointer',
            backend_tools.Cursors.POINTER: 'default',
            backend_tools.Cursors.SELECT_REGION: 'crosshair',
            backend_tools.Cursors.MOVE: 'move',
            backend_tools.Cursors.WAIT: 'wait',
            backend_tools.Cursors.RESIZE_HORIZONTAL: 'ew-resize',
            backend_tools.Cursors.RESIZE_VERTICAL: 'ns-resize',
        }, cursor=cursor)
        self.send_event('cursor', cursor=cursor)

    def set_image_mode(self, mode):
        """
        Set the image mode for any subsequent images which will be sent
        to the clients. The modes may currently be either 'full' or 'diff'.

        Note: diff images may not contain transparency, therefore upon
        draw this mode may be changed if the resulting image has any
        transparent component.
        """
        _api.check_in_list(['full', 'diff'], mode=mode)
        if self._current_image_mode != mode:
            self._current_image_mode = mode
            self.handle_send_image_mode(None)

    def get_diff_image(self):
        if self._png_is_old:
            renderer = self.get_renderer()

            pixels = np.asarray(renderer.buffer_rgba())
            # The buffer is created as type uint32 so that entire
            # pixels can be compared in one numpy call, rather than
            # needing to compare each plane separately.
            buff = pixels.view(np.uint32).squeeze(2)

            if (self._force_full
                    # If the buffer has changed size we need to do a full draw.
                    or buff.shape != self._last_buff.shape
                    # If any pixels have transparency, we need to force a full
                    # draw as we cannot overlay new on top of old.
                    or (pixels[:, :, 3] != 255).any()):
                self.set_image_mode('full')
                output = buff
            else:
                self.set_image_mode('diff')
                diff = buff != self._last_buff
                output = np.where(diff, buff, 0)

            # Store the current buffer so we can compute the next diff.
            self._last_buff = buff.copy()
            self._force_full = False
            self._png_is_old = False

            data = output.view(dtype=np.uint8).reshape((*output.shape, 4))
            with BytesIO() as png:
                Image.fromarray(data).save(png, format="png")
                return png.getvalue()

    def handle_event(self, event):
        e_type = event['type']
        handler = getattr(self, 'handle_{0}'.format(e_type),
                          self.handle_unknown_event)
        return handler(event)

    def handle_unknown_event(self, event):
        _log.warning('Unhandled message type {0}. {1}'.format(
                     event['type'], event))

    def handle_ack(self, event):
        # Network latency tends to decrease if traffic is flowing
        # in both directions.  Therefore, the browser sends back
        # an "ack" message after each image frame is received.
        # This could also be used as a simple sanity check in the
        # future, but for now the performance increase is enough
        # to justify it, even if the server does nothing with it.
        pass

    def handle_draw(self, event):
        self.draw()

    def _handle_mouse(self, event):
        x = event['x']
        y = event['y']
        y = self.get_renderer().height - y
        self._last_mouse_xy = x, y
        # JavaScript button numbers and Matplotlib button numbers are off by 1.
        button = event['button'] + 1

        e_type = event['type']
        guiEvent = event.get('guiEvent')
        if e_type in ['button_press', 'button_release']:
            MouseEvent(e_type + '_event', self, x, y, button,
                       guiEvent=guiEvent)._process()
        elif e_type == 'dblclick':
            MouseEvent('button_press_event', self, x, y, button, dblclick=True,
                       guiEvent=guiEvent)._process()
        elif e_type == 'scroll':
            MouseEvent('scroll_event', self, x, y, step=event['step'],
                       guiEvent=guiEvent)._process()
        elif e_type == 'motion_notify':
            MouseEvent(e_type + '_event', self, x, y,
                       guiEvent=guiEvent)._process()
        elif e_type in ['figure_enter', 'figure_leave']:
            LocationEvent(e_type + '_event', self, x, y,
                          guiEvent=guiEvent)._process()
    handle_button_press = handle_button_release = handle_dblclick = \
        handle_figure_enter = handle_figure_leave = handle_motion_notify = \
        handle_scroll = _handle_mouse

    def _handle_key(self, event):
        KeyEvent(event['type'] + '_event', self,
                 _handle_key(event['key']), *self._last_mouse_xy,
                 guiEvent=event.get('guiEvent'))._process()
    handle_key_press = handle_key_release = _handle_key

    def handle_toolbar_button(self, event):
        # TODO: Be more suspicious of the input
        getattr(self.toolbar, event['name'])()

    def handle_refresh(self, event):
        figure_label = self.figure.get_label()
        if not figure_label:
            figure_label = "Figure {0}".format(self.manager.num)
        self.send_event('figure_label', label=figure_label)
        self._force_full = True
        if self.toolbar:
            # Normal toolbar init would refresh this, but it happens before the
            # browser canvas is set up.
            self.toolbar.set_history_buttons()
        self.draw_idle()

    def handle_resize(self, event):
        x = int(event.get('width', 800)) * self.device_pixel_ratio
        y = int(event.get('height', 800)) * self.device_pixel_ratio
        fig = self.figure
        # An attempt at approximating the figure size in pixels.
        fig.set_size_inches(x / fig.dpi, y / fig.dpi, forward=False)
        # Acknowledge the resize, and force the viewer to update the
        # canvas size to the figure's new size (which is hopefully
        # identical or within a pixel or so).
        self._png_is_old = True
        self.manager.resize(*fig.bbox.size, forward=False)
        ResizeEvent('resize_event', self)._process()
        self.draw_idle()

    def handle_send_image_mode(self, event):
        # The client requests notification of what the current image mode is.
        self.send_event('image_mode', mode=self._current_image_mode)

    def handle_set_device_pixel_ratio(self, event):
        self._handle_set_device_pixel_ratio(event.get('device_pixel_ratio', 1))

    def handle_set_dpi_ratio(self, event):
        # This handler is for backwards-compatibility with older ipympl.
        self._handle_set_device_pixel_ratio(event.get('dpi_ratio', 1))

    def _handle_set_device_pixel_ratio(self, device_pixel_ratio):
        if self._set_device_pixel_ratio(device_pixel_ratio):
            self._force_full = True
            self.draw_idle()

    def send_event(self, event_type, **kwargs):
        if self.manager:
            self.manager._send_event(event_type, **kwargs)
