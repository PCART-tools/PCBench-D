    def __init__(self, canvas, num):
        FigureManagerBase.__init__(self, canvas, num)
        self.canvas = canvas
        self.window = MainWindow()
        self.window.closing.connect(canvas.close_event)
        self.window.closing.connect(self._widgetclosed)

        self.window.setWindowTitle("Figure %d" % num)
        image = str(cbook._get_data_path('images/matplotlib.svg'))
        self.window.setWindowIcon(QtGui.QIcon(image))

        # Give the keyboard focus to the figure instead of the
        # manager; StrongFocus accepts both tab and click to focus and
        # will enable the canvas to process event w/o clicking.
        # ClickFocus only takes the focus is the window has been
        # clicked
        # on. http://qt-project.org/doc/qt-4.8/qt.html#FocusPolicy-enum or
        # http://doc.qt.digia.com/qt/qt.html#FocusPolicy-enum
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas.setFocus()

        self.window._destroying = False

        self.toolmanager = self._get_toolmanager()
        self.toolbar = self._get_toolbar(self.canvas, self.window)
        self.statusbar = None

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)
                self.statusbar = StatusbarQt(self.window, self.toolmanager)

        if self.toolbar is not None:
            self.window.addToolBar(self.toolbar)
            if not self.toolmanager:
                # add text label to status bar
                statusbar_label = QtWidgets.QLabel()
                self.window.statusBar().addWidget(statusbar_label)
                self.toolbar.message.connect(statusbar_label.setText)
            tbs_height = self.toolbar.sizeHint().height()
        else:
            tbs_height = 0

        # resize the main window so it will display the canvas with the
        # requested size:
        cs = canvas.sizeHint()
        sbs = self.window.statusBar().sizeHint()
        height = cs.height() + tbs_height + sbs.height()
        self.window.resize(cs.width(), height)

        self.window.setCentralWidget(self.canvas)

        if matplotlib.is_interactive():
            self.window.show()
            self.canvas.draw_idle()

        self.window.raise_()
