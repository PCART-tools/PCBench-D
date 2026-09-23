    def _get_groupframe(self, group):
        if group not in self._groups:
            if self._groups:
                self._add_separator()
            frame = Tk.Frame(master=self, borderwidth=0)
            frame.pack(side=Tk.LEFT, fill=Tk.Y)
            self._groups[group] = frame
        return self._groups[group]
