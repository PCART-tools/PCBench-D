class NavigationToolbar2Wx(NavigationToolbar2, wx.ToolBar):
    def __init__(self, canvas):
        wx.ToolBar.__init__(self, canvas.GetParent(), -1)
        NavigationToolbar2.__init__(self, canvas)
        self.canvas = canvas
        self._idle = True
        self.statbar = None
        self.prevZoomRect = None
        # for now, use alternate zoom-rectangle drawing on all
        # Macs. N.B. In future versions of wx it may be possible to
        # detect Retina displays with window.GetContentScaleFactor()
        # and/or dc.GetContentScaleFactor()
        self.retinaFix = 'wxMac' in wx.PlatformInfo

    def get_canvas(self, frame, fig):
        return type(self.canvas)(frame, -1, fig)

    def _init_toolbar(self):
        DEBUG_MSG("_init_toolbar", 1, self)

        self._parent = self.canvas.GetParent()

        self.wx_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.AddSeparator()
                continue
            self.wx_ids[text] = (
                self.AddTool(
                    -1,
                    bitmap=_load_bitmap(image_file + ".png"),
                    bmpDisabled=wx.NullBitmap,
                    label=text, shortHelp=text, longHelp=tooltip_text,
                    kind=(wx.ITEM_CHECK if text in ["Pan", "Zoom"]
                          else wx.ITEM_NORMAL))
                .Id)
            self.Bind(wx.EVT_TOOL, getattr(self, callback),
                      id=self.wx_ids[text])

        self.Realize()

    def zoom(self, *args):
        self.ToggleTool(self.wx_ids['Pan'], False)
        NavigationToolbar2.zoom(self, *args)

    def pan(self, *args):
        self.ToggleTool(self.wx_ids['Zoom'], False)
        NavigationToolbar2.pan(self, *args)

    def configure_subplots(self, evt):
        global FigureManager  # placates pyflakes: created by @_Backend.export
        frame = wx.Frame(None, -1, "Configure subplots")
        _set_frame_icon(frame)

        toolfig = Figure((6, 3))
        canvas = self.get_canvas(frame, toolfig)

        # Create a figure manager to manage things
        figmgr = FigureManager(canvas, 1, frame)

        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        frame.SetSizer(sizer)
        frame.Fit()
        tool = SubplotTool(self.canvas.figure, toolfig)
        frame.Show()

    def save_figure(self, *args):
        # Fetch the required filename and file type.
        filetypes, exts, filter_index = self.canvas._get_imagesave_wildcards()
        default_file = self.canvas.get_default_filename()
        dlg = wx.FileDialog(self._parent, "Save to file", "", default_file,
                            filetypes,
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        dlg.SetFilterIndex(filter_index)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
            DEBUG_MSG(
                'Save file dir:%s name:%s' %
                (dirname, filename), 3, self)
            format = exts[dlg.GetFilterIndex()]
            basename, ext = os.path.splitext(filename)
            if ext.startswith('.'):
                ext = ext[1:]
            if ext in ('svg', 'pdf', 'ps', 'eps', 'png') and format != ext:
                # looks like they forgot to set the image type drop
                # down, going with the extension.
                warnings.warn(
                    'extension %s did not match the selected '
                    'image type %s; going with %s' %
                    (ext, format, ext), stacklevel=2)
                format = ext
            try:
                self.canvas.figure.savefig(
                    os.path.join(dirname, filename), format=format)
            except Exception as e:
                error_msg_wx(str(e))

    def set_cursor(self, cursor):
        cursor = wx.Cursor(cursord[cursor])
        self.canvas.SetCursor(cursor)
        self.canvas.Update()

    def press(self, event):
        if self._active == 'ZOOM':
            if not self.retinaFix:
                self.wxoverlay = wx.Overlay()
            else:
                if event.inaxes is not None:
                    self.savedRetinaImage = self.canvas.copy_from_bbox(
                        event.inaxes.bbox)
                    self.zoomStartX = event.xdata
                    self.zoomStartY = event.ydata
                    self.zoomAxes = event.inaxes

    def release(self, event):
        if self._active == 'ZOOM':
            # When the mouse is released we reset the overlay and it
            # restores the former content to the window.
            if not self.retinaFix:
                self.wxoverlay.Reset()
                del self.wxoverlay
            else:
                del self.savedRetinaImage
                if self.prevZoomRect:
                    self.prevZoomRect.pop(0).remove()
                    self.prevZoomRect = None
                if self.zoomAxes:
                    self.zoomAxes = None

    def draw_rubberband(self, event, x0, y0, x1, y1):
        if self.retinaFix:  # On Macs, use the following code
            # wx.DCOverlay does not work properly on Retina displays.
            rubberBandColor = '#C0C0FF'
            if self.prevZoomRect:
                self.prevZoomRect.pop(0).remove()
            self.canvas.restore_region(self.savedRetinaImage)
            X0, X1 = self.zoomStartX, event.xdata
            Y0, Y1 = self.zoomStartY, event.ydata
            lineX = (X0, X0, X1, X1, X0)
            lineY = (Y0, Y1, Y1, Y0, Y0)
            self.prevZoomRect = self.zoomAxes.plot(
                lineX, lineY, '-', color=rubberBandColor)
            self.zoomAxes.draw_artist(self.prevZoomRect[0])
            self.canvas.blit(self.zoomAxes.bbox)
            return

        # Use an Overlay to draw a rubberband-like bounding box.

        dc = wx.ClientDC(self.canvas)
        odc = wx.DCOverlay(self.wxoverlay, dc)
        odc.Clear()

        # Mac's DC is already the same as a GCDC, and it causes
        # problems with the overlay if we try to use an actual
        # wx.GCDC so don't try it.
        if 'wxMac' not in wx.PlatformInfo:
            dc = wx.GCDC(dc)

        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0

        if y1 < y0:
            y0, y1 = y1, y0
        if x1 < x0:
            x0, x1 = x1, x0

        w = x1 - x0
        h = y1 - y0
        rect = wx.Rect(x0, y0, w, h)

        rubberBandColor = '#C0C0FF'  # or load from config?

        # Set a pen for the border
        color = wx.Colour(rubberBandColor)
        dc.SetPen(wx.Pen(color, 1))

        # use the same color, plus alpha for the brush
        r, g, b, a = color.Get(True)
        color.Set(r, g, b, 0x60)
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(rect)

    def set_status_bar(self, statbar):
        self.statbar = statbar

    def set_message(self, s):
        if self.statbar is not None:
            self.statbar.set_function(s)

    def set_history_buttons(self):
        can_backward = self._nav_stack._pos > 0
        can_forward = self._nav_stack._pos < len(self._nav_stack._elements) - 1
        self.EnableTool(self.wx_ids['Back'], can_backward)
        self.EnableTool(self.wx_ids['Forward'], can_forward)
