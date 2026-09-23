class _FigureCanvasWxBase(FigureCanvasBase, wx.Panel):
    """
    The FigureCanvas contains the figure and does event handling.

    In the wxPython backend, it is derived from wxPanel, and (usually) lives
    inside a frame instantiated by a FigureManagerWx. The parent window
    probably implements a wx.Sizer to control the displayed control size - but
    we give a hint as to our preferred minimum size.
    """

    keyvald = {
        wx.WXK_CONTROL: 'control',
        wx.WXK_SHIFT: 'shift',
        wx.WXK_ALT: 'alt',
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

    def __init__(self, parent, id, figure):
        """
        Initialise a FigureWx instance.

        - Initialise the FigureCanvasBase and wxPanel parents.
        - Set event handlers for:
          EVT_SIZE  (Resize event)
          EVT_PAINT (Paint event)
        """

        FigureCanvasBase.__init__(self, figure)
        # Set preferred window size hint - helps the sizer (if one is
        # connected)
        l, b, w, h = figure.bbox.bounds
        w = math.ceil(w)
        h = math.ceil(h)

        wx.Panel.__init__(self, parent, id, size=wx.Size(w, h))

        # Create the drawing bitmap
        self.bitmap = wx.Bitmap(w, h)
        DEBUG_MSG("__init__() - bitmap w:%d h:%d" % (w, h), 2, self)
        # TODO: Add support for 'point' inspection and plot navigation.
        self._isDrawn = False

        self.Bind(wx.EVT_SIZE, self._onSize)
        self.Bind(wx.EVT_PAINT, self._onPaint)
        self.Bind(wx.EVT_KEY_DOWN, self._onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self._onKeyUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self._onRightButtonDown)
        self.Bind(wx.EVT_RIGHT_DCLICK, self._onRightButtonDClick)
        self.Bind(wx.EVT_RIGHT_UP, self._onRightButtonUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self._onMouseWheel)
        self.Bind(wx.EVT_LEFT_DOWN, self._onLeftButtonDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self._onLeftButtonDClick)
        self.Bind(wx.EVT_LEFT_UP, self._onLeftButtonUp)
        self.Bind(wx.EVT_MOTION, self._onMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._onLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self._onEnter)
        # Add middle button events
        self.Bind(wx.EVT_MIDDLE_DOWN, self._onMiddleButtonDown)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self._onMiddleButtonDClick)
        self.Bind(wx.EVT_MIDDLE_UP, self._onMiddleButtonUp)

        self.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self._onCaptureLost)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self._onCaptureLost)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)  # Reduce flicker.
        self.SetBackgroundColour(wx.WHITE)

    @property
    @cbook.deprecated("3.0")
    def macros(self):
        return {}

    def Copy_to_Clipboard(self, event=None):
        "copy bitmap of canvas to system clipboard"
        bmp_obj = wx.BitmapDataObject()
        bmp_obj.SetBitmap(self.bitmap)

        if not wx.TheClipboard.IsOpened():
            open_success = wx.TheClipboard.Open()
            if open_success:
                wx.TheClipboard.SetData(bmp_obj)
                wx.TheClipboard.Close()
                wx.TheClipboard.Flush()

    def draw_idle(self):
        """
        Delay rendering until the GUI is idle.
        """
        DEBUG_MSG("draw_idle()", 1, self)
        self._isDrawn = False  # Force redraw
        # Triggering a paint event is all that is needed to defer drawing
        # until later. The platform will send the event when it thinks it is
        # a good time (usually as soon as there are no other events pending).
        self.Refresh(eraseBackground=False)

    def new_timer(self, *args, **kwargs):
        """
        Creates a new backend-specific subclass of
        :class:`backend_bases.Timer`. This is useful for getting periodic
        events through the backend's native event loop. Implemented only
        for backends with GUIs.

        Other Parameters
        ----------------
        interval : scalar
            Timer interval in milliseconds
        callbacks : list
            Sequence of (func, args, kwargs) where ``func(*args, **kwargs)``
            will be executed by the timer every *interval*.

        """
        return TimerWx(*args, **kwargs)

    def flush_events(self):
        wx.Yield()

    def start_event_loop(self, timeout=0):
        """
        Start an event loop.  This is used to start a blocking event
        loop so that interactive functions, such as ginput and
        waitforbuttonpress, can wait for events.  This should not be
        confused with the main GUI event loop, which is always running
        and has nothing to do with this.

        This call blocks until a callback function triggers
        stop_event_loop() or *timeout* is reached.  If *timeout* is
        <=0, never timeout.

        Raises RuntimeError if event loop is already running.
        """
        if hasattr(self, '_event_loop'):
            raise RuntimeError("Event loop already running")
        id = wx.NewId()
        timer = wx.Timer(self, id=id)
        if timeout > 0:
            timer.Start(timeout * 1000, oneShot=True)
            self.Bind(wx.EVT_TIMER, self.stop_event_loop, id=id)

        # Event loop handler for start/stop event loop
        self._event_loop = wx.GUIEventLoop()
        self._event_loop.Run()
        timer.Stop()

    def stop_event_loop(self, event=None):
        """
        Stop an event loop.  This is used to stop a blocking event
        loop so that interactive functions, such as ginput and
        waitforbuttonpress, can wait for events.

        """
        if hasattr(self, '_event_loop'):
            if self._event_loop.IsRunning():
                self._event_loop.Exit()
            del self._event_loop

    def _get_imagesave_wildcards(self):
        'return the wildcard string for the filesave dialog'
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

    def gui_repaint(self, drawDC=None, origin='WX'):
        """
        Performs update of the displayed image on the GUI canvas, using the
        supplied wx.PaintDC device context.

        The 'WXAgg' backend sets origin accordingly.
        """
        DEBUG_MSG("gui_repaint()", 1, self)
        if self.IsShownOnScreen():
            if not drawDC:
                # not called from OnPaint use a ClientDC
                drawDC = wx.ClientDC(self)

            # following is for 'WX' backend on Windows
            # the bitmap can not be in use by another DC,
            # see GraphicsContextWx._cache
            if wx.Platform == '__WXMSW__' and origin == 'WX':
                img = self.bitmap.ConvertToImage()
                bmp = img.ConvertToBitmap()
                drawDC.DrawBitmap(bmp, 0, 0)
            else:
                drawDC.DrawBitmap(self.bitmap, 0, 0)

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
        super().print_figure(filename, *args, **kwargs)
        # Restore the current view; this is needed because the artist contains
        # methods rely on particular attributes of the rendered figure for
        # determining things like bounding boxes.
        if self._isDrawn:
            self.draw()

    def _onPaint(self, evt):
        """
        Called when wxPaintEvt is generated
        """

        DEBUG_MSG("_onPaint()", 1, self)
        drawDC = wx.PaintDC(self)
        if not self._isDrawn:
            self.draw(drawDC=drawDC)
        else:
            self.gui_repaint(drawDC=drawDC)
        drawDC.Destroy()

    def _onSize(self, evt):
        """
        Called when wxEventSize is generated.

        In this application we attempt to resize to fit the window, so it
        is better to take the performance hit and redraw the whole window.
        """

        DEBUG_MSG("_onSize()", 2, self)
        sz = self.GetParent().GetSizer()
        if sz:
            si = sz.GetItem(self)
        if sz and si and not si.Proportion and not si.Flag & wx.EXPAND:
            # managed by a sizer, but with a fixed size
            size = self.GetMinSize()
        else:
            # variable size
            size = self.GetClientSize()
        if getattr(self, "_width", None):
            if size == (self._width, self._height):
                # no change in size
                return
        self._width, self._height = size
        # Create a new, correctly sized bitmap
        self.bitmap = wx.Bitmap(self._width, self._height)

        self._isDrawn = False

        if self._width <= 1 or self._height <= 1:
            return  # Empty figure

        dpival = self.figure.dpi
        winch = self._width / dpival
        hinch = self._height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)

        # Rendering will happen on the associated paint event
        # so no need to do anything here except to make sure
        # the whole background is repainted.
        self.Refresh(eraseBackground=False)
        FigureCanvasBase.resize_event(self)

    def _get_key(self, evt):

        keyval = evt.KeyCode
        if keyval in self.keyvald:
            key = self.keyvald[keyval]
        elif keyval < 256:
            key = chr(keyval)
            # wx always returns an uppercase, so make it lowercase if the shift
            # key is not depressed (NOTE: this will not handle Caps Lock)
            if not evt.ShiftDown():
                key = key.lower()
        else:
            key = None

        for meth, prefix in (
                [evt.AltDown, 'alt'],
                [evt.ControlDown, 'ctrl'], ):
            if meth():
                key = '{0}+{1}'.format(prefix, key)

        return key

    def _onKeyDown(self, evt):
        """Capture key press."""
        key = self._get_key(evt)
        FigureCanvasBase.key_press_event(self, key, guiEvent=evt)
        if self:
            evt.Skip()

    def _onKeyUp(self, evt):
        """Release key."""
        key = self._get_key(evt)
        FigureCanvasBase.key_release_event(self, key, guiEvent=evt)
        if self:
            evt.Skip()

    def _set_capture(self, capture=True):
        """control wx mouse capture """
        if self.HasCapture():
            self.ReleaseMouse()
        if capture:
            self.CaptureMouse()

    def _onCaptureLost(self, evt):
        """Capture changed or lost"""
        self._set_capture(False)

    def _onRightButtonDown(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(True)
        FigureCanvasBase.button_press_event(self, x, y, 3, guiEvent=evt)

    def _onRightButtonDClick(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(True)
        FigureCanvasBase.button_press_event(self, x, y, 3,
                                            dblclick=True, guiEvent=evt)

    def _onRightButtonUp(self, evt):
        """End measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(False)
        FigureCanvasBase.button_release_event(self, x, y, 3, guiEvent=evt)

    def _onLeftButtonDown(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(True)
        FigureCanvasBase.button_press_event(self, x, y, 1, guiEvent=evt)

    def _onLeftButtonDClick(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(True)
        FigureCanvasBase.button_press_event(self, x, y, 1,
                                            dblclick=True, guiEvent=evt)

    def _onLeftButtonUp(self, evt):
        """End measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(False)
        FigureCanvasBase.button_release_event(self, x, y, 1, guiEvent=evt)

    # Add middle button events
    def _onMiddleButtonDown(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(True)
        FigureCanvasBase.button_press_event(self, x, y, 2, guiEvent=evt)

    def _onMiddleButtonDClick(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(True)
        FigureCanvasBase.button_press_event(self, x, y, 2,
                                            dblclick=True, guiEvent=evt)

    def _onMiddleButtonUp(self, evt):
        """End measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(False)
        FigureCanvasBase.button_release_event(self, x, y, 2, guiEvent=evt)

    def _onMouseWheel(self, evt):
        """Translate mouse wheel events into matplotlib events"""

        # Determine mouse location
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()

        # Convert delta/rotation/rate into a floating point step size
        delta = evt.GetWheelDelta()
        rotation = evt.GetWheelRotation()
        rate = evt.GetLinesPerAction()
        step = rate * rotation / delta

        # Done handling event
        evt.Skip()

        # Mac is giving two events for every wheel event
        # Need to skip every second one
        if wx.Platform == '__WXMAC__':
            if not hasattr(self, '_skipwheelevent'):
                self._skipwheelevent = True
            elif self._skipwheelevent:
                self._skipwheelevent = False
                return  # Return without processing event
            else:
                self._skipwheelevent = True

        # Convert to mpl event
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=evt)

    def _onMotion(self, evt):
        """Start measuring on an axis."""

        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=evt)

    def _onLeave(self, evt):
        """Mouse has left the window."""

        evt.Skip()
        FigureCanvasBase.leave_notify_event(self, guiEvent=evt)

    def _onEnter(self, evt):
        """Mouse has entered the window."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        FigureCanvasBase.enter_notify_event(self, guiEvent=evt, xy=(x, y))
