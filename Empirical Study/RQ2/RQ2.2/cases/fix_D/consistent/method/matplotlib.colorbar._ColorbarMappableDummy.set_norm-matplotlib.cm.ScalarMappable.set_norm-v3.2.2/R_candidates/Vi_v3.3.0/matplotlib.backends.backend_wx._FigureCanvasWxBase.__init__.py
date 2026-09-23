    def __init__(self, parent, id, figure):
        """
        Initialize a FigureWx instance.

        - Initialize the FigureCanvasBase and wxPanel parents.
        - Set event handlers for resize, paint, and keyboard and mouse
          interaction.
        """

        FigureCanvasBase.__init__(self, figure)
        w, h = map(math.ceil, figure.bbox.size)
        # Set preferred window size hint - helps the sizer, if one is connected
        wx.Panel.__init__(self, parent, id, size=wx.Size(w, h))
        # Create the drawing bitmap
        self.bitmap = wx.Bitmap(w, h)
        _log.debug("%s - __init__() - bitmap w:%d h:%d", type(self), w, h)
        # TODO: Add support for 'point' inspection and plot navigation.
        self._isDrawn = False

        self.Bind(wx.EVT_SIZE, self._onSize)
        self.Bind(wx.EVT_PAINT, self._onPaint)
        self.Bind(wx.EVT_KEY_DOWN, self._onKeyDown)
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
