    def _add_to_group(self, group, name, button, position):
        gr = self._groups.get(group, [])
        if not gr:
            sep = self.addSeparator()
            gr.append(sep)
        before = gr[position]
        widget = self.insertWidget(before, button)
        gr.insert(position, widget)
        self._groups[group] = gr
