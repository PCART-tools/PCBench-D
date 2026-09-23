    def draw(self):
        super(FigureCanvasTkAgg, self).draw()
        _backend_tk.blit(self._tkphoto, self.renderer._renderer, (0, 1, 2, 3))
        self._master.update_idletasks()
