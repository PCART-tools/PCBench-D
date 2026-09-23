class FigureCanvasQT(QtWidgets.QWidget, FigureCanvasBase):
    required_interactive_framework = "qt5"
    _timer_cls = TimerQT

    # map Qt button codes to MouseEvent's ones:
    buttond = {QtCore.Qt.LeftButton: MouseButton.LEFT,
               QtCore.Qt.MidButton: MouseButton.MIDDLE,
               QtCore.Qt.RightButton: MouseButton.RIGHT,
               QtCore.Qt.XButton1: MouseButton.BACK,
               QtCore.Qt.XButton2: MouseButton.FORWARD,
               }

    @_allow_super_init
    def __init__(self, figure=None):
        _create_qApp()
        super().__init__(figure=figure)

        # We don't want to scale up the figure DPI more than once.
        # Note, we don't handle a signal for changing DPI yet.
        self.figure._original_dpi = self.figure.dpi
        self._update_figure_dpi()
        # In cases with mixed resolution displays, we need to be careful if the
        # dpi_ratio changes - in this case we need to resize the canvas
        # accordingly.
        self._dpi_ratio_prev = self._dpi_ratio

        self._draw_pending = False
        self._is_drawing = False
        self._draw_rect_callback = lambda painter: None

        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setMouseTracking(True)
        self.resize(*self.get_width_height())

        palette = QtGui.QPalette(QtCore.Qt.white)
        self.setPalette(palette)

    def _update_figure_dpi(self):
        dpi = self._dpi_ratio * self.figure._original_dpi
        self.figure._set_dpi(dpi, forward=False)

    @property
    def _dpi_ratio(self):
        return _devicePixelRatioF(self)

    def _update_pixel_ratio(self):
        # We need to be careful in cases with mixed resolution displays if
        # dpi_ratio changes.
        if self._dpi_ratio != self._dpi_ratio_prev:
            # We need to update the figure DPI.
            self._update_figure_dpi()
            self._dpi_ratio_prev = self._dpi_ratio
            # The easiest way to resize the canvas is to emit a resizeEvent
            # since we implement all the logic for resizing the canvas for
            # that event.
            event = QtGui.QResizeEvent(self.size(), self.size())
            self.resizeEvent(event)
            # resizeEvent triggers a paintEvent itself, so we exit this one
            # (after making sure that the event is immediately handled).

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

    def get_width_height(self):
        w, h = FigureCanvasBase.get_width_height(self)
        return int(w / self._dpi_ratio), int(h / self._dpi_ratio)

    def enterEvent(self, event):
        try:
            x, y = self.mouseEventCoords(event.pos())
        except AttributeError:
            # the event from PyQt4 does not include the position
            x = y = None
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        FigureCanvasBase.leave_notify_event(self, guiEvent=event)

    def mouseEventCoords(self, pos):
        """
        Calculate mouse coordinates in physical pixels.

        Qt5 use logical pixels, but the figure is scaled to physical
        pixels for rendering.  Transform to physical pixels so that
        all of the down-stream transforms work as expected.

        Also, the origin is different and needs to be corrected.
        """
        dpi_ratio = self._dpi_ratio
        x = pos.x()
        # flip y so y=0 is bottom of canvas
        y = self.figure.bbox.height / dpi_ratio - pos.y()
        return x * dpi_ratio, y * dpi_ratio

    def mousePressEvent(self, event):
        x, y = self.mouseEventCoords(event.pos())
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_press_event(self, x, y, button,
                                                guiEvent=event)

    def mouseDoubleClickEvent(self, event):
        x, y = self.mouseEventCoords(event.pos())
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_press_event(self, x, y,
                                                button, dblclick=True,
                                                guiEvent=event)

    def mouseMoveEvent(self, event):
        x, y = self.mouseEventCoords(event)
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)

    def mouseReleaseEvent(self, event):
        x, y = self.mouseEventCoords(event)
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_release_event(self, x, y, button,
                                                  guiEvent=event)

    if QtCore.qVersion() >= "5.":
        def wheelEvent(self, event):
            x, y = self.mouseEventCoords(event)
            # from QWheelEvent::delta doc
            if event.pixelDelta().x() == 0 and event.pixelDelta().y() == 0:
                steps = event.angleDelta().y() / 120
            else:
                steps = event.pixelDelta().y()
            if steps:
                FigureCanvasBase.scroll_event(
                    self, x, y, steps, guiEvent=event)
    else:
        def wheelEvent(self, event):
            x = event.x()
            # flipy so y=0 is bottom of canvas
            y = self.figure.bbox.height - event.y()
            # from QWheelEvent::delta doc
            steps = event.delta() / 120
            if event.orientation() == QtCore.Qt.Vertical:
                FigureCanvasBase.scroll_event(
                    self, x, y, steps, guiEvent=event)

    def keyPressEvent(self, event):
        key = self._get_key(event)
        if key is not None:
            FigureCanvasBase.key_press_event(self, key, guiEvent=event)

    def keyReleaseEvent(self, event):
        key = self._get_key(event)
        if key is not None:
            FigureCanvasBase.key_release_event(self, key, guiEvent=event)

    def resizeEvent(self, event):
        w = event.size().width() * self._dpi_ratio
        h = event.size().height() * self._dpi_ratio
        dpival = self.figure.dpi
        winch = w / dpival
        hinch = h / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        # pass back into Qt to let it finish
        QtWidgets.QWidget.resizeEvent(self, event)
        # emit our resize events
        FigureCanvasBase.resize_event(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minumumSizeHint(self):
        return QtCore.QSize(10, 10)

    def _get_key(self, event):
        event_key = event.key()
        event_mods = int(event.modifiers())  # actually a bitmask

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
            # key, rather than unicode
            key = SPECIAL_KEYS[event_key]
        except KeyError:
            # unicode defines code points up to 0x10ffff (sys.maxunicode)
            # QT will use Key_Codes larger than that for keyboard keys that are
            # are not unicode characters (like multimedia keys)
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
        qApp.processEvents()

    def start_event_loop(self, timeout=0):
        # docstring inherited
        if hasattr(self, "_event_loop") and self._event_loop.isRunning():
            raise RuntimeError("Event loop already running")
        self._event_loop = event_loop = QtCore.QEventLoop()
        if timeout > 0:
            timer = QtCore.QTimer.singleShot(int(timeout * 1000),
                                             event_loop.quit)
        event_loop.exec_()

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
        l, b, w, h = [int(pt / self._dpi_ratio) for pt in bbox.bounds]
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
            x0, y0, w, h = [int(pt / self._dpi_ratio) for pt in rect]
            x1 = x0 + w
            y1 = y0 + h
            def _draw_rect_callback(painter):
                pen = QtGui.QPen(QtCore.Qt.black, 1 / self._dpi_ratio)
                pen.setDashPattern([3, 3])
                for color, offset in [
                        (QtCore.Qt.black, 0), (QtCore.Qt.white, 3)]:
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
