class _FigureCanvasWxBase(FigureCanvasBase, wx.Panel):
    """
    The FigureCanvas contains the figure and does event handling.

    In the wxPython backend, it is derived from wxPanel, and (usually) lives
    inside a frame instantiated by a FigureManagerWx. The parent window
    probably implements a wx.Sizer to control the displayed control size - but
    we give a hint as to our preferred minimum size.
    """

    required_interactive_framework = "wx"
    _timer_cls = TimerWx

    keyvald = {
        wx.WXK_CONTROL: 'control',
        wx.WXK_SHIFT: 'shift',
        wx.WXK_ALT: 'alt',
        wx.WXK_CAPITAL: 'caps_lock',
        wx.WXK_LEFT: 'left',
        wx.WXK_UP: 'up',
        wx.WXK_RIGHT: 'right',
        wx.WXK_DOWN: 'down',
        wx.WXK_ESCAPE: 'escape',
        wx.WXK_F1: 'f1',
        wx.WXK_F2: 'f2',
        wx.WXK_F3: 'f3',
        wx.WXK_F4: 'f4',
        wx.WXK_F5: 'f5',
        wx.WXK_F6: 'f6',
        wx.WXK_F7: 'f7',
        wx.WXK_F8: 'f8',
        wx.WXK_F9: 'f9',
        wx.WXK_F10: 'f10',
        wx.WXK_F11: 'f11',
        wx.WXK_F12: 'f12',
        wx.WXK_SCROLL: 'scroll_lock',
        wx.WXK_PAUSE: 'break',
        wx.WXK_BACK: 'backspace',
        wx.WXK_RETURN: 'enter',
        wx.WXK_INSERT: 'insert',
        wx.WXK_DELETE: 'delete',
        wx.WXK_HOME: 'home',
        wx.WXK_END: 'end',
        wx.WXK_PAGEUP: 'pageup',
        wx.WXK_PAGEDOWN: 'pagedown',
        wx.WXK_NUMPAD0: '0',
        wx.WXK_NUMPAD1: '1',
        wx.WXK_NUMPAD2: '2',
        wx.WXK_NUMPAD3: '3',
        wx.WXK_NUMPAD4: '4',
        wx.WXK_NUMPAD5: '5',
        wx.WXK_NUMPAD6: '6',
        wx.WXK_NUMPAD7: '7',
        wx.WXK_NUMPAD8: '8',
        wx.WXK_NUMPAD9: '9',
        wx.WXK_NUMPAD_ADD: '+',
        wx.WXK_NUMPAD_SUBTRACT: '-',
        wx.WXK_NUMPAD_MULTIPLY: '*',
        wx.WXK_NUMPAD_DIVIDE: '/',
        wx.WXK_NUMPAD_DECIMAL: 'dec',
        wx.WXK_NUMPAD_ENTER: 'enter',
        wx.WXK_NUMPAD_UP: 'up',
        wx.WXK_NUMPAD_RIGHT: 'right',
        wx.WXK_NUMPAD_DOWN: 'down',
        wx.WXK_NUMPAD_LEFT: 'left',
        wx.WXK_NUMPAD_PAGEUP: 'pageup',
        wx.WXK_NUMPAD_PAGEDOWN: 'pagedown',
        wx.WXK_NUMPAD_HOME: 'home',
        wx.WXK_NUMPAD_END: 'end',
        wx.WXK_NUMPAD_INSERT: 'insert',
        wx.WXK_NUMPAD_DELETE: 'delete',
    }

    def __init__(self, parent, id, figure=None):
        """
        Initialize a FigureWx instance.

        - Initialize the FigureCanvasBase and wxPanel parents.
        - Set event handlers for resize, paint, and keyboard and mouse
          interaction.
        """

        FigureCanvasBase.__init__(self, figure)
        w, h = map(math.ceil, self.figure.bbox.size)
        # Set preferred window size hint - helps the sizer, if one is connected
        wx.Panel.__init__(self, parent, id, size=wx.Size(w, h))
        # Create the drawing bitmap
        self.bitmap = wx.Bitmap(w, h)
        _log.debug("%s - __init__() - bitmap w:%d h:%d", type(self), w, h)
        self._isDrawn = False
        self._rubberband_rect = None

        self.Bind(wx.EVT_SIZE, self._onSize)
        self.Bind(wx.EVT_PAINT, self._onPaint)
        self.Bind(wx.EVT_CHAR_HOOK, self._onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self._onKeyUp)
        self.Bind(wx.EVT_LEFT_DOWN, self._onMouseButton)
        self.Bind(wx.EVT_LEFT_DCLICK, self._onMouseButton)
        self.Bind(wx.EVT_LEFT_UP, self._onMouseButton)
        self.Bind(wx.EVT_MIDDLE_DOWN, self._onMouseButton)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self._onMouseButton)
        self.Bind(wx.EVT_MIDDLE_UP, self._onMouseButton)
        self.Bind(wx.EVT_RIGHT_DOWN, self._onMouseButton)
        self.Bind(wx.EVT_RIGHT_DCLICK, self._onMouseButton)
        self.Bind(wx.EVT_RIGHT_UP, self._onMouseButton)
        self.Bind(wx.EVT_MOUSEWHEEL, self._onMouseWheel)
        self.Bind(wx.EVT_MOTION, self._onMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self._onEnter)

        self.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self._onCaptureLost)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self._onCaptureLost)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)  # Reduce flicker.
        self.SetBackgroundColour(wx.WHITE)

    def Copy_to_Clipboard(self, event=None):
        """Copy bitmap of canvas to system clipboard."""
        bmp_obj = wx.BitmapDataObject()
        bmp_obj.SetBitmap(self.bitmap)

        if not wx.TheClipboard.IsOpened():
            open_success = wx.TheClipboard.Open()
            if open_success:
                wx.TheClipboard.SetData(bmp_obj)
                wx.TheClipboard.Close()
                wx.TheClipboard.Flush()

    def draw_idle(self):
        # docstring inherited
        _log.debug("%s - draw_idle()", type(self))
        self._isDrawn = False  # Force redraw
        # Triggering a paint event is all that is needed to defer drawing
        # until later. The platform will send the event when it thinks it is
        # a good time (usually as soon as there are no other events pending).
        self.Refresh(eraseBackground=False)

    def flush_events(self):
        # docstring inherited
        wx.Yield()

    def start_event_loop(self, timeout=0):
        # docstring inherited
        if hasattr(self, '_event_loop'):
            raise RuntimeError("Event loop already running")
        timer = wx.Timer(self, id=wx.ID_ANY)
        if timeout > 0:
            timer.Start(int(timeout * 1000), oneShot=True)
            self.Bind(wx.EVT_TIMER, self.stop_event_loop, id=timer.GetId())
        # Event loop handler for start/stop event loop
        self._event_loop = wx.GUIEventLoop()
        self._event_loop.Run()
        timer.Stop()

    def stop_event_loop(self, event=None):
        # docstring inherited
        if hasattr(self, '_event_loop'):
            if self._event_loop.IsRunning():
                self._event_loop.Exit()
            del self._event_loop

    def _get_imagesave_wildcards(self):
        """Return the wildcard string for the filesave dialog."""
        default_filetype = self.get_default_filetype()
        filetypes = self.get_supported_filetypes_grouped()
        sorted_filetypes = sorted(filetypes.items())
        wildcards = []
        extensions = []
        filter_index = 0
        for i, (name, exts) in enumerate(sorted_filetypes):
            ext_list = ';'.join(['*.%s' % ext for ext in exts])
            extensions.append(exts[0])
            wildcard = '%s (%s)|%s' % (name, ext_list, ext_list)
            if default_filetype in exts:
                filter_index = i
            wildcards.append(wildcard)
        wildcards = '|'.join(wildcards)
        return wildcards, extensions, filter_index

    @_api.delete_parameter("3.4", "origin")
    def gui_repaint(self, drawDC=None, origin='WX'):
        """
        Performs update of the displayed image on the GUI canvas, using the
        supplied wx.PaintDC device context.

        The 'WXAgg' backend sets origin accordingly.
        """
        _log.debug("%s - gui_repaint()", type(self))
        # The "if self" check avoids a "wrapped C/C++ object has been deleted"
        # RuntimeError if doing things after window is closed.
        if not (self and self.IsShownOnScreen()):
            return
        if not drawDC:  # not called from OnPaint use a ClientDC
            drawDC = wx.ClientDC(self)
        # For 'WX' backend on Windows, the bitmap can not be in use by another
        # DC (see GraphicsContextWx._cache).
        bmp = (self.bitmap.ConvertToImage().ConvertToBitmap()
               if wx.Platform == '__WXMSW__'
                  and isinstance(self.figure._cachedRenderer, RendererWx)
               else self.bitmap)
        drawDC.DrawBitmap(bmp, 0, 0)
        if self._rubberband_rect is not None:
            x0, y0, x1, y1 = self._rubberband_rect
            drawDC.DrawLineList(
                [(x0, y0, x1, y0), (x1, y0, x1, y1),
                 (x0, y0, x0, y1), (x0, y1, x1, y1)],
                wx.Pen('BLACK', 1, wx.PENSTYLE_SHORT_DASH))

    filetypes = {
        **FigureCanvasBase.filetypes,
        'bmp': 'Windows bitmap',
        'jpeg': 'JPEG',
        'jpg': 'JPEG',
        'pcx': 'PCX',
        'png': 'Portable Network Graphics',
        'tif': 'Tagged Image Format File',
        'tiff': 'Tagged Image Format File',
        'xpm': 'X pixmap',
    }

    def print_figure(self, filename, *args, **kwargs):
        # docstring inherited
        super().print_figure(filename, *args, **kwargs)
        # Restore the current view; this is needed because the artist contains
        # methods rely on particular attributes of the rendered figure for
        # determining things like bounding boxes.
        if self._isDrawn:
            self.draw()

    def _onPaint(self, event):
        """Called when wxPaintEvt is generated."""
        _log.debug("%s - _onPaint()", type(self))
        drawDC = wx.PaintDC(self)
        if not self._isDrawn:
            self.draw(drawDC=drawDC)
        else:
            self.gui_repaint(drawDC=drawDC)
        drawDC.Destroy()

    def _onSize(self, event):
        """
        Called when wxEventSize is generated.

        In this application we attempt to resize to fit the window, so it
        is better to take the performance hit and redraw the whole window.
        """

        _log.debug("%s - _onSize()", type(self))
        sz = self.GetParent().GetSizer()
        if sz:
            si = sz.GetItem(self)
        if sz and si and not si.Proportion and not si.Flag & wx.EXPAND:
            # managed by a sizer, but with a fixed size
            size = self.GetMinSize()
        else:
            # variable size
            size = self.GetClientSize()
            # Do not allow size to become smaller than MinSize
            size.IncTo(self.GetMinSize())
        if getattr(self, "_width", None):
            if size == (self._width, self._height):
                # no change in size
                return
        self._width, self._height = size
        self._isDrawn = False

        if self._width <= 1 or self._height <= 1:
            return  # Empty figure

        # Create a new, correctly sized bitmap
        self.bitmap = wx.Bitmap(self._width, self._height)

        dpival = self.figure.dpi
        winch = self._width / dpival
        hinch = self._height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)

        # Rendering will happen on the associated paint event
        # so no need to do anything here except to make sure
        # the whole background is repainted.
        self.Refresh(eraseBackground=False)
        FigureCanvasBase.resize_event(self)

    def _get_key(self, event):

        keyval = event.KeyCode
        if keyval in self.keyvald:
            key = self.keyvald[keyval]
        elif keyval < 256:
            key = chr(keyval)
            # wx always returns an uppercase, so make it lowercase if the shift
            # key is not depressed (NOTE: this will not handle Caps Lock)
            if not event.ShiftDown():
                key = key.lower()
        else:
            key = None

        for meth, prefix, key_name in (
                [event.ControlDown, 'ctrl', 'control'],
                [event.AltDown, 'alt', 'alt'],
                [event.ShiftDown, 'shift', 'shift'],):
            if meth() and key_name != key:
                if not (key_name == 'shift' and key.isupper()):
                    key = '{0}+{1}'.format(prefix, key)

        return key

    def _onKeyDown(self, event):
        """Capture key press."""
        key = self._get_key(event)
        FigureCanvasBase.key_press_event(self, key, guiEvent=event)
        if self:
            event.Skip()

    def _onKeyUp(self, event):
        """Release key."""
        key = self._get_key(event)
        FigureCanvasBase.key_release_event(self, key, guiEvent=event)
        if self:
            event.Skip()

    def _set_capture(self, capture=True):
        """Control wx mouse capture."""
        if self.HasCapture():
            self.ReleaseMouse()
        if capture:
            self.CaptureMouse()

    def _onCaptureLost(self, event):
        """Capture changed or lost"""
        self._set_capture(False)

    def _onMouseButton(self, event):
        """Start measuring on an axis."""
        event.Skip()
        self._set_capture(event.ButtonDown() or event.ButtonDClick())
        x = event.X
        y = self.figure.bbox.height - event.Y
        button_map = {
            wx.MOUSE_BTN_LEFT: MouseButton.LEFT,
            wx.MOUSE_BTN_MIDDLE: MouseButton.MIDDLE,
            wx.MOUSE_BTN_RIGHT: MouseButton.RIGHT,
        }
        button = event.GetButton()
        button = button_map.get(button, button)
        if event.ButtonDown():
            self.button_press_event(x, y, button, guiEvent=event)
        elif event.ButtonDClick():
            self.button_press_event(x, y, button, dblclick=True,
                                    guiEvent=event)
        elif event.ButtonUp():
            self.button_release_event(x, y, button, guiEvent=event)

    def _onMouseWheel(self, event):
        """Translate mouse wheel events into matplotlib events"""
        # Determine mouse location
        x = event.GetX()
        y = self.figure.bbox.height - event.GetY()
        # Convert delta/rotation/rate into a floating point step size
        step = event.LinesPerAction * event.WheelRotation / event.WheelDelta
        # Done handling event
        event.Skip()
        # Mac gives two events for every wheel event; skip every second one.
        if wx.Platform == '__WXMAC__':
            if not hasattr(self, '_skipwheelevent'):
                self._skipwheelevent = True
            elif self._skipwheelevent:
                self._skipwheelevent = False
                return  # Return without processing event
            else:
                self._skipwheelevent = True
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)

    def _onMotion(self, event):
        """Start measuring on an axis."""
        x = event.GetX()
        y = self.figure.bbox.height - event.GetY()
        event.Skip()
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)

    def _onLeave(self, event):
        """Mouse has left the window."""
        event.Skip()
        FigureCanvasBase.leave_notify_event(self, guiEvent=event)

    def _onEnter(self, event):
        """Mouse has entered the window."""
        x = event.GetX()
        y = self.figure.bbox.height - event.GetY()
        event.Skip()
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))
