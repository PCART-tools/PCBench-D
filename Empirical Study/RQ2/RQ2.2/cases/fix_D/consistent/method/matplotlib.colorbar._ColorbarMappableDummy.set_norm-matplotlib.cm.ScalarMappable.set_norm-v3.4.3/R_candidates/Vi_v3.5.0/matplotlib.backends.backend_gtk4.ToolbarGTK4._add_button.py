    def _add_button(self, button, group, position):
        if group not in self._groups:
            if self._groups:
                self._add_separator()
            group_box = Gtk.Box()
            self._tool_box.append(group_box)
            self._groups[group] = group_box
        self._groups[group].insert_child_after(
            button, self._find_child_at_position(group, position))
