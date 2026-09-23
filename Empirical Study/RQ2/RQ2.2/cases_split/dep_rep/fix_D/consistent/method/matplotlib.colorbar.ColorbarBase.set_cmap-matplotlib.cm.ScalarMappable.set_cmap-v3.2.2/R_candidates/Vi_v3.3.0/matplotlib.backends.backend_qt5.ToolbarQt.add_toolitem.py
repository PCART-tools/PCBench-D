    def add_toolitem(
            self, name, group, position, image_file, description, toggle):

        button = QtWidgets.QToolButton(self)
        button.setIcon(NavigationToolbar2QT._icon(self, image_file))
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
