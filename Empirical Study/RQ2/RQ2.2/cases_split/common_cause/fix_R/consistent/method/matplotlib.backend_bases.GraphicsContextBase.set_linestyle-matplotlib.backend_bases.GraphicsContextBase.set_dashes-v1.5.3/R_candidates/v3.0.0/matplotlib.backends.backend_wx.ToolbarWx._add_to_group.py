    def _add_to_group(self, group, name, position):
        gr = self._groups.get(group, [])
        if not gr:
            sep = self.AddSeparator()
            gr.append(sep)
        before = gr[position]
        self._groups[group] = gr
        return before, gr
