    def add_toolitem(
            self, name, group, position, image_file, description, toggle):
        frame = self._get_groupframe(group)
        buttons = frame.pack_slaves()
        if position >= len(buttons) or position < 0:
            before = None
        else:
            before = buttons[position]
        button = NavigationToolbar2Tk._Button(frame, name, image_file, toggle,
                                              lambda: self._button_click(name))
        button.pack_configure(before=before)
        if description is not None:
            add_tooltip(button, description)
        self._toolitems.setdefault(name, [])
        self._toolitems[name].append(button)
