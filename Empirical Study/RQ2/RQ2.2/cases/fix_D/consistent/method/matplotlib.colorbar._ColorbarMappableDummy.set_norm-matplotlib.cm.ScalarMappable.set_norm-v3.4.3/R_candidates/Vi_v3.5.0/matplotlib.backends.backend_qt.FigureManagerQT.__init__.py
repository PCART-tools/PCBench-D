    def __init__(self, canvas, num):
        self.window = MainWindow()
        super().__init__(canvas, num)
        self.window.closing.connect(canvas.close_event)
        self.window.closing.connect(self._widgetclosed)

        image = str(cbook._get_data_path('images/matplotlib.svg'))
        self.window.setWindowIcon(QtGui.QIcon(image))

        self.window._destroying = False

        self.toolbar = self._get_toolbar(self.canvas, self.window)

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)

        if self.toolbar:
            self.window.addToolBar(self.toolbar)
            tbs_height = self.toolbar.sizeHint().height()
        else:
            tbs_height = 0

        # resize the main window so it will display the canvas with the
        # requested size:
        cs = canvas.sizeHint()
        cs_height = cs.height()
        height = cs_height + tbs_height
        self.window.resize(cs.width(), height)

        self.window.setCentralWidget(self.canvas)

        if mpl.is_interactive():
            self.window.show()
            self.canvas.draw_idle()

        # Give the keyboard focus to the figure instead of the manager:
        # StrongFocus accepts both tab and click to focus and will enable the
        # canvas to process event without clicking.
        # https://doc.qt.io/qt-5/qt.html#FocusPolicy-enum
        self.canvas.setFocusPolicy(_enum("QtCore.Qt.FocusPolicy").StrongFocus)
        self.canvas.setFocus()

        self.window.raise_()
