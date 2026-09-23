class ToolbarQt(ToolContainerBase, QtWidgets.QToolBar):
    def __init__(self, toolmanager, parent):
        ToolContainerBase.__init__(self, toolmanager)
        QtWidgets.QToolBar.__init__(self, parent)
        self._toolitems = {}
        self._groups = {}

    @property
    def _icon_extension(self):
        if is_pyqt5():
            return '_large.png'
        return '.png'

    def add_toolitem(
            self, name, group, position, image_file, description, toggle):

        button = QtWidgets.QToolButton(self)
        button.setIcon(self._icon(image_file))
        button.setText(name)
        if description:
            button.setToolTip(description)

        def handler():
            self.trigger_tool(name)
        if toggle:
            button.setCheckable(True)
            button.toggled.connect(handler)
        else:
            button.clicked.connect(handler)

        self._toolitems.setdefault(name, [])
        self._add_to_group(group, name, button, position)
        self._toolitems[name].append((button, handler))

    def _add_to_group(self, group, name, button, position):
        gr = self._groups.get(group, [])
        if not gr:
            sep = self.addSeparator()
            gr.append(sep)
        before = gr[position]
        widget = self.insertWidget(before, button)
        gr.insert(position, widget)
        self._groups[group] = gr

    def _icon(self, name):
        pm = QtGui.QPixmap(name)
        if hasattr(pm, 'setDevicePixelRatio'):
            pm.setDevicePixelRatio(self.toolmanager.canvas._dpi_ratio)
        return QtGui.QIcon(pm)

    def toggle_toolitem(self, name, toggled):
        if name not in self._toolitems:
            return
        for button, handler in self._toolitems[name]:
            button.toggled.disconnect(handler)
            button.setChecked(toggled)
            button.toggled.connect(handler)

    def remove_toolitem(self, name):
        for button, handler in self._toolitems[name]:
            button.setParent(None)
        del self._toolitems[name]
