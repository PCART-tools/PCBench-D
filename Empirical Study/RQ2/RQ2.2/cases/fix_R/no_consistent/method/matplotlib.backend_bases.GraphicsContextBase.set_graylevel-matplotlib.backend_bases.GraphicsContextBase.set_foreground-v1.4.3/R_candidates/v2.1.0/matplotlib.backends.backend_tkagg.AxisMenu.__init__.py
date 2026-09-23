    def __init__(self, master, naxes):
        self._master = master
        self._naxes = naxes
        self._mbar = Tk.Frame(master=master, relief=Tk.RAISED, borderwidth=2)
        self._mbar.pack(side=Tk.LEFT)
        self._mbutton = Tk.Menubutton(
            master=self._mbar, text="Axes", underline=0)
        self._mbutton.pack(side=Tk.LEFT, padx="2m")
        self._mbutton.menu = Tk.Menu(self._mbutton)
        self._mbutton.menu.add_command(
            label="Select All", command=self.select_all)
        self._mbutton.menu.add_command(
            label="Invert All", command=self.invert_all)
        self._axis_var = []
        self._checkbutton = []
        for i in range(naxes):
            self._axis_var.append(Tk.IntVar())
            self._axis_var[i].set(1)
            self._checkbutton.append(self._mbutton.menu.add_checkbutton(
                label = "Axis %d" % (i+1),
                variable=self._axis_var[i],
                command=self.set_active))
            self._mbutton.menu.invoke(self._mbutton.menu.index("Select All"))
        self._mbutton['menu'] = self._mbutton.menu
        self._mbar.tk_menuBar(self._mbutton)
        self.set_active()
