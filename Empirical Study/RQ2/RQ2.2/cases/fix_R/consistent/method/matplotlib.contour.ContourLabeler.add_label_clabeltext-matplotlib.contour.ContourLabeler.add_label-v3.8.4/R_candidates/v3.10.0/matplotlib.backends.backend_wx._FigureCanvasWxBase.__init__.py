    def __init__(self, parent, id, figure=None):
        """
        Initialize a FigureWx instance.

        - Initialize the FigureCanvasBase and wxPanel parents.
        - Set event handlers for resize, paint, and keyboard and mouse
          interaction.
        """

        FigureCanvasBase.__init__(self, figure)
        size = wx.Size(*map(math.ceil, self.figure.bbox.size))
        if wx.Platform != '__WXMSW__':
            size = parent.FromDIP(size)
        # Set preferred window size hint - helps the sizer, if one is connected
        wx.Panel.__init__(self, parent, id, size=size)
        self.bitmap = None
        self._isDrawn = False
        self._rubberband_rect = None
        self._rubberband_pen_black = wx.Pen('BLACK', 1, wx.PENSTYLE_SHORT_DASH)
        self._rubberband_pen_white = wx.Pen('WHITE', 1, wx.PENSTYLE_SOLID)

        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key_down)
        self.Bind(wx.EVT_KEY_UP, self._on_key_up)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_button)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_mouse_button)
        self.Bind(wx.EVT_LEFT_UP, self._on_mouse_button)
        self.Bind(wx.EVT_MIDDLE_DOWN, self._on_mouse_button)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self._on_mouse_button)
        self.Bind(wx.EVT_MIDDLE_UP, self._on_mouse_button)
        self.Bind(wx.EVT_RIGHT_DOWN, self._on_mouse_button)
        self.Bind(wx.EVT_RIGHT_DCLICK, self._on_mouse_button)
        self.Bind(wx.EVT_RIGHT_UP, self._on_mouse_button)
        self.Bind(wx.EVT_MOUSE_AUX1_DOWN, self._on_mouse_button)
        self.Bind(wx.EVT_MOUSE_AUX1_UP, self._on_mouse_button)
        self.Bind(wx.EVT_MOUSE_AUX2_DOWN, self._on_mouse_button)
        self.Bind(wx.EVT_MOUSE_AUX2_UP, self._on_mouse_button)
        self.Bind(wx.EVT_MOUSE_AUX1_DCLICK, self._on_mouse_button)
        self.Bind(wx.EVT_MOUSE_AUX2_DCLICK, self._on_mouse_button)
        self.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse_wheel)
        self.Bind(wx.EVT_MOTION, self._on_motion)
        self.Bind(wx.EVT_ENTER_WINDOW, self._on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._on_leave)

        self.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self._on_capture_lost)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self._on_capture_lost)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)  # Reduce flicker.
        self.SetBackgroundColour(wx.WHITE)

        if wx.Platform == '__WXMAC__':
            # Initial scaling. Other platforms handle this automatically
            dpiScale = self.GetDPIScaleFactor()
            self.SetInitialSize(self.GetSize()*(1/dpiScale))
            self._set_device_pixel_ratio(dpiScale)
