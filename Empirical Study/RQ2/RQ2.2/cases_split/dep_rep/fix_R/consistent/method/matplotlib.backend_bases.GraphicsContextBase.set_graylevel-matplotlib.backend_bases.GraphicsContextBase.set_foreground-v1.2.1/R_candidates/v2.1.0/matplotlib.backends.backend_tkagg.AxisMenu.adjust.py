    def adjust(self, naxes):
        if self._naxes < naxes:
            for i in range(self._naxes, naxes):
                self._axis_var.append(Tk.IntVar())
                self._axis_var[i].set(1)
                self._checkbutton.append( self._mbutton.menu.add_checkbutton(
                    label = "Axis %d" % (i+1),
                    variable=self._axis_var[i],
                    command=self.set_active))
        elif self._naxes > naxes:
            for i in range(self._naxes-1, naxes-1, -1):
                del self._axis_var[i]
                self._mbutton.menu.forget(self._checkbutton[i])
                del self._checkbutton[i]
        self._naxes = naxes
        self.set_active()
