    def draw(self):
        # Note: FigureCanvasBase.draw() is inconveniently named as it clashes
        # with the deprecated gtk.Widget.draw()

        self._need_redraw = True
        if GTK_WIDGET_DRAWABLE(self):
            self.queue_draw()
            # do a synchronous draw (its less efficient than an async draw,
            # but is required if/when animation is used)
            self.window.process_updates (False)
