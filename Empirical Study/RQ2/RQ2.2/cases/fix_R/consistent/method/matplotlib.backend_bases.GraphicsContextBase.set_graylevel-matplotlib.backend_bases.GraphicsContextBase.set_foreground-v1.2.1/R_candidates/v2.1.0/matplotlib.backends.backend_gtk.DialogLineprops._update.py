    def _update(self):
        'update the active line props from the widgets'
        if not self._inited or not self._updateson: return
        line = self.get_active_line()
        ls = self.get_active_linestyle()
        marker = self.get_active_marker()
        line.set_linestyle(ls)
        line.set_marker(marker)

        button = self.wtree.get_widget('colorbutton_linestyle')
        color = button.get_color()
        r, g, b = [val/65535. for val in (color.red, color.green, color.blue)]
        line.set_color((r,g,b))

        button = self.wtree.get_widget('colorbutton_markerface')
        color = button.get_color()
        r, g, b = [val/65535. for val in (color.red, color.green, color.blue)]
        line.set_markerfacecolor((r,g,b))

        line.figure.canvas.draw()
