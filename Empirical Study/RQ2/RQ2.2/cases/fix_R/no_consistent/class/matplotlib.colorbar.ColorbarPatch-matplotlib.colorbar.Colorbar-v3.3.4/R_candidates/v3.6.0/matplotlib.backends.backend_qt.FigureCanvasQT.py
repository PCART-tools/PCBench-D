class FigureCanvasQT(FigureCanvasBase, QtWidgets.QWidget):
    required_interactive_framework = "qt"
    _timer_cls = TimerQT
    manager_class = _api.classproperty(lambda cls: FigureManagerQT)

    buttond = {
        getattr(_enum("QtCore.Qt.MouseButton"), k): v for k, v in [
            ("LeftButton", MouseButton.LEFT),
            ("RightButton", MouseButton.RIGHT),
            ("MiddleButton", MouseButton.MIDDLE),
            ("XButton1", MouseButton.BACK),
            ("XButton2", MouseButton.FORWARD),
        ]
    }

    def __init__(self, figure=None):
        _create_qApp()
        super().__init__(figure=figure)

        self._draw_pending = False
        self._is_drawing = False
        self._draw_rect_callback = lambda painter: None
        self._in_resize_event = False

        self.setAttribute(
            _enum("QtCore.Qt.WidgetAttribute").WA_OpaquePaintEvent)
        self.setMouseTracking(True)
        self.resize(*self.get_width_height())

        palette = QtGui.QPalette(QtGui.QColor("white"))
        self.setPalette(palette)

    def _update_pixel_ratio(self):
        if self._set_device_pixel_ratio(_devicePixelRatioF(self)):
            # The easiest way to resize the canvas is to emit a resizeEvent
            # since we implement all the logic for resizing the canvas for
            # that event.
            event = QtGui.QResizeEvent(self.size(), self.size())
            self.resizeEvent(event)

    def _update_screen(self, screen):
        # Handler for changes to a window's attached screen.
        self._update_pixel_ratio()
        if screen is not None:
            screen.physicalDotsPerInchChanged.connect(self._update_pixel_ratio)
            screen.logicalDotsPerInchChanged.connect(self._update_pixel_ratio)

    def showEvent(self, event):
        # Set up correct pixel ratio, and connect to any signal changes for it,
        # once the window is shown (and thus has these attributes).
        window = self.window().windowHandle()
        window.screenChanged.connect(self._update_screen)
        self._update_screen(window.screen())

    def set_cursor(self, cursor):
        # docstring inherited
        self.setCursor(_api.check_getitem(cursord, cursor=cursor))

    def mouseEventCoords(self, pos=None):
        """
        Calculate mouse coordinates in physical pixels.

        Qt uses logical pixels, but the figure is scaled to physical
        pixels for rendering.  Transform to physical pixels so that
        all of the down-stream transforms work as expected.

        Also, the origin is different and needs to be corrected.
        """
        if pos is None:
            pos = self.mapFromGlobal(QtGui.QCursor.pos())
        elif hasattr(pos, "position"):  # qt6 QtGui.QEvent
            pos = pos.position()
        elif hasattr(pos, "pos"):  # qt5 QtCore.QEvent
            pos = pos.pos()
        # (otherwise, it's already a QPoint)
        x = pos.x()
        # flip y so y=0 is bottom of canvas
        y = self.figure.bbox.height / self.device_pixel_ratio - pos.y()
        return x * self.device_pixel_ratio, y * self.device_pixel_ratio

    def enterEvent(self, event):
        LocationEvent("figure_enter_event", self,
                      *self.mouseEventCoords(event),
                      guiEvent=event)._process()

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        LocationEvent("figure_leave_event", self,
                      *self.mouseEventCoords(),
                      guiEvent=event)._process()

    def mousePressEvent(self, event):
        button = self.buttond.get(event.button())
        if button is not None:
            MouseEvent("button_press_event", self,
                       *self.mouseEventCoords(event), button,
                       guiEvent=event)._process()

    def mouseDoubleClickEvent(self, event):
        button = self.buttond.get(event.button())
        if button is not None:
            MouseEvent("button_press_event", self,
                       *self.mouseEventCoords(event), button, dblclick=True,
                       guiEvent=event)._process()

    def mouseMoveEvent(self, event):
        MouseEvent("motion_notify_event", self,
                   *self.mouseEventCoords(event),
                   guiEvent=event)._process()

    def mouseReleaseEvent(self, event):
        button = self.buttond.get(event.button())
        if button is not None:
            MouseEvent("button_release_event", self,
                       *self.mouseEventCoords(event), button,
                       guiEvent=event)._process()

    def wheelEvent(self, event):
        # from QWheelEvent::pixelDelta doc: pixelDelta is sometimes not
        # provided (`isNull()`) and is unreliable on X11 ("xcb").
        if (event.pixelDelta().isNull()
                or QtWidgets.QApplication.instance().platformName() == "xcb"):
            steps = event.angleDelta().y() / 120
        else:
            steps = event.pixelDelta().y()
        if steps:
            MouseEvent("scroll_event", self,
                       *self.mouseEventCoords(event), step=steps,
                       guiEvent=event)._process()

    def keyPressEvent(self, event):
        key = self._get_key(event)
        if key is not None:
            KeyEvent("key_press_event", self,
                     key, *self.mouseEventCoords(),
                     guiEvent=event)._process()

    def keyReleaseEvent(self, event):
        key = self._get_key(event)
        if key is not None:
            KeyEvent("key_release_event", self,
                     key, *self.mouseEventCoords(),
                     guiEvent=event)._process()

    def resizeEvent(self, event):
        if self._in_resize_event:  # Prevent PyQt6 recursion
            return
        self._in_resize_event = True
        try:
            w = event.size().width() * self.device_pixel_ratio
            h = event.size().height() * self.device_pixel_ratio
            dpival = self.figure.dpi
            winch = w / dpival
            hinch = h / dpival
            self.figure.set_size_inches(winch, hinch, forward=False)
            # pass back into Qt to let it finish
            QtWidgets.QWidget.resizeEvent(self, event)
            # emit our resize events
            ResizeEvent("resize_event", self)._process()
            self.draw_idle()
        finally:
            self._in_resize_event = False

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minumumSizeHint(self):
        return QtCore.QSize(10, 10)

    def _get_key(self, event):
        event_key = event.key()
        event_mods = _to_int(event.modifiers())  # actually a bitmask

        # get names of the pressed modifier keys
        # 'control' is named 'control' when a standalone key, but 'ctrl' when a
        # modifier
        # bit twiddling to pick out modifier keys from event_mods bitmask,
        # if event_key is a MODIFIER, it should not be duplicated in mods
        mods = [SPECIAL_KEYS[key].replace('control', 'ctrl')
                for mod, key in _MODIFIER_KEYS
                if event_key != key and event_mods & mod]
        try:
            # for certain keys (enter, left, backspace, etc) use a word for the
            # key, rather than Unicode
            key = SPECIAL_KEYS[event_key]
        except KeyError:
            # Unicode defines code points up to 0x10ffff (sys.maxunicode)
            # QT will use Key_Codes larger than that for keyboard keys that are
            # are not Unicode characters (like multimedia keys)
            # skip these
            # if you really want them, you should add them to SPECIAL_KEYS
            if event_key > sys.maxunicode:
                return None

            key = chr(event_key)
            # qt delivers capitalized letters.  fix capitalization
            # note that capslock is ignored
            if 'shift' in mods:
                mods.remove('shift')
            else:
                key = key.lower()

        return '+'.join(mods + [key])

    def flush_events(self):
        # docstring inherited
        QtWidgets.QApplication.instance().processEvents()

    def start_event_loop(self, timeout=0):
        # docstring inherited
        if hasattr(self, "_event_loop") and self._event_loop.isRunning():
            raise RuntimeError("Event loop already running")
        self._event_loop = event_loop = QtCore.QEventLoop()
        if timeout > 0:
            _ = QtCore.QTimer.singleShot(int(timeout * 1000), event_loop.quit)

        with _maybe_allow_interrupt(event_loop):
            qt_compat._exec(event_loop)

    def stop_event_loop(self, event=None):
        # docstring inherited
        if hasattr(self, "_event_loop"):
            self._event_loop.quit()

    def draw(self):
        """Render the figure, and queue a request for a Qt draw."""
        # The renderer draw is done here; delaying causes problems with code
        # that uses the result of the draw() to update plot elements.
        if self._is_drawing:
            return
        with cbook._setattr_cm(self, _is_drawing=True):
            super().draw()
        self.update()

    def draw_idle(self):
        """Queue redraw of the Agg buffer and request Qt paintEvent."""
        # The Agg draw needs to be handled by the same thread Matplotlib
        # modifies the scene graph from. Post Agg draw request to the
        # current event loop in order to ensure thread affinity and to
        # accumulate multiple draw requests from event handling.
        # TODO: queued signal connection might be safer than singleShot
        if not (getattr(self, '_draw_pending', False) or
                getattr(self, '_is_drawing', False)):
            self._draw_pending = True
            QtCore.QTimer.singleShot(0, self._draw_idle)

    def blit(self, bbox=None):
        # docstring inherited
        if bbox is None and self.figure:
            bbox = self.figure.bbox  # Blit the entire canvas if bbox is None.
        # repaint uses logical pixels, not physical pixels like the renderer.
        l, b, w, h = [int(pt / self.device_pixel_ratio) for pt in bbox.bounds]
        t = b + h
        self.repaint(l, self.rect().height() - t, w, h)

    def _draw_idle(self):
        with self._idle_draw_cntx():
            if not self._draw_pending:
                return
            self._draw_pending = False
            if self.height() < 0 or self.width() < 0:
                return
            try:
                self.draw()
            except Exception:
                # Uncaught exceptions are fatal for PyQt5, so catch them.
                traceback.print_exc()

    def drawRectangle(self, rect):
        # Draw the zoom rectangle to the QPainter.  _draw_rect_callback needs
        # to be called at the end of paintEvent.
        if rect is not None:
            x0, y0, w, h = [int(pt / self.device_pixel_ratio) for pt in rect]
            x1 = x0 + w
            y1 = y0 + h
            def _draw_rect_callback(painter):
                pen = QtGui.QPen(
                    QtGui.QColor("black"),
                    1 / self.device_pixel_ratio
                )

                pen.setDashPattern([3, 3])
                for color, offset in [
                        (QtGui.QColor("black"), 0),
                        (QtGui.QColor("white"), 3),
                ]:
                    pen.setDashOffset(offset)
                    pen.setColor(color)
                    painter.setPen(pen)
                    # Draw the lines from x0, y0 towards x1, y1 so that the
                    # dashes don't "jump" when moving the zoom box.
                    painter.drawLine(x0, y0, x0, y1)
                    painter.drawLine(x0, y0, x1, y0)
                    painter.drawLine(x0, y1, x1, y1)
                    painter.drawLine(x1, y0, x1, y1)
        else:
            def _draw_rect_callback(painter):
                return
        self._draw_rect_callback = _draw_rect_callback
        self.update()
