    def on_combobox_lineprops_changed(self, item):
        'update the widgets from the active line'
        if not self._inited: return
        self._updateson = False
        line = self.get_active_line()

        ls = line.get_linestyle()
        if ls is None: ls = 'None'
        self.cbox_linestyles.set_active(self.linestyled[ls])

        marker = line.get_marker()
        if marker is None: marker = 'None'
        self.cbox_markers.set_active(self.markerd[marker])

        rgba = mcolors.to_rgba(line.get_color())
        color = gtk.gdk.Color(*[int(val*65535) for val in rgba[:3]])
        button = self.wtree.get_widget('colorbutton_linestyle')
        button.set_color(color)

        rgba = mcolors.to_rgba(line.get_markerfacecolor())
        color = gtk.gdk.Color(*[int(val*65535) for val in rgba[:3]])
        button = self.wtree.get_widget('colorbutton_markerface')
        button.set_color(color)
        self._updateson = True
