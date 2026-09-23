    def add_toolitem(
            self, name, group, position, image_file, description, toggle):
        frame = self._get_groupframe(group)
        button = NavigationToolbar2Tk._Button(self, name, image_file, toggle,
                                              lambda: self._button_click(name))
        if description is not None:
            ToolTip.createToolTip(button, description)
        self._toolitems.setdefault(name, [])
        self._toolitems[name].append(button)
