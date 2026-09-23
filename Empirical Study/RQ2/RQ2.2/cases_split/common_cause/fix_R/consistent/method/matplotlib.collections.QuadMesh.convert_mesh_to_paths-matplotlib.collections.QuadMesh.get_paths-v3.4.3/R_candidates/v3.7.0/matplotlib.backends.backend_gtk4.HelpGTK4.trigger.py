    def trigger(self, *args):
        section = Gtk.ShortcutsSection()

        for name, tool in sorted(self.toolmanager.tools.items()):
            if not tool.description:
                continue

            # Putting everything in a separate group allows GTK to
            # automatically split them into separate columns/pages, which is
            # useful because we have lots of shortcuts, some with many keys
            # that are very wide.
            group = Gtk.ShortcutsGroup()
            section.append(group)
            # A hack to remove the title since we have no group naming.
            child = group.get_first_child()
            while child is not None:
                child.set_visible(False)
                child = child.get_next_sibling()

            shortcut = Gtk.ShortcutsShortcut(
                accelerator=' '.join(
                    self._normalize_shortcut(key)
                    for key in self.toolmanager.get_tool_keymap(name)
                    if self._is_valid_shortcut(key)),
                title=tool.name,
                subtitle=tool.description)
            group.append(shortcut)

        window = Gtk.ShortcutsWindow(
            title='Help',
            modal=True,
            transient_for=self._figure.canvas.get_root())
        window.set_child(section)

        window.show()
