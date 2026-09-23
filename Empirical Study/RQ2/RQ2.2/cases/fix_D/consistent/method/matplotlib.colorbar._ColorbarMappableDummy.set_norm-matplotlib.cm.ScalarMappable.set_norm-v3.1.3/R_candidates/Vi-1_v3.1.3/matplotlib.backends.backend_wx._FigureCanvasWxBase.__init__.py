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
