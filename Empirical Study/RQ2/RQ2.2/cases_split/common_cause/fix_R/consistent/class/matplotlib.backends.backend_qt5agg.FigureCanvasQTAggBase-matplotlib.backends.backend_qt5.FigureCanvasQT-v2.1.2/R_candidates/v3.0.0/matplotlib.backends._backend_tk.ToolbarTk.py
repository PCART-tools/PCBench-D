class ToolbarTk(ToolContainerBase, Tk.Frame):
    _icon_extension = '.gif'
    def __init__(self, toolmanager, window):
        ToolContainerBase.__init__(self, toolmanager)
        xmin, xmax = self.toolmanager.canvas.figure.bbox.intervalx
        height, width = 50, xmax - xmin
        Tk.Frame.__init__(self, master=window,
                          width=int(width), height=int(height),
                          borderwidth=2)
        self._toolitems = {}
        self.pack(side=Tk.TOP, fill=Tk.X)
        self._groups = {}

    def add_toolitem(
            self, name, group, position, image_file, description, toggle):
        frame = self._get_groupframe(group)
        button = self._Button(name, image_file, toggle, frame)
        if description is not None:
            ToolTip.createToolTip(button, description)
        self._toolitems.setdefault(name, [])
        self._toolitems[name].append(button)

    def _get_groupframe(self, group):
        if group not in self._groups:
            if self._groups:
                self._add_separator()
            frame = Tk.Frame(master=self, borderwidth=0)
            frame.pack(side=Tk.LEFT, fill=Tk.Y)
            self._groups[group] = frame
        return self._groups[group]

    def _add_separator(self):
        separator = Tk.Frame(master=self, bd=5, width=1, bg='black')
        separator.pack(side=Tk.LEFT, fill=Tk.Y, padx=2)

    def _Button(self, text, image_file, toggle, frame):
        if image_file is not None:
            im = Tk.PhotoImage(master=self, file=image_file)
        else:
            im = None

        if not toggle:
            b = Tk.Button(master=frame, text=text, padx=2, pady=2, image=im,
                          command=lambda: self._button_click(text))
        else:
            # There is a bug in tkinter included in some python 3.6 versions
            # that without this variable, produces a "visual" toggling of
            # other near checkbuttons
            # https://bugs.python.org/issue29402
            # https://bugs.python.org/issue25684
            var = Tk.IntVar()
            b = Tk.Checkbutton(master=frame, text=text, padx=2, pady=2,
                               image=im, indicatoron=False,
                               command=lambda: self._button_click(text),
                               variable=var)
        b._ntimage = im
        b.pack(side=Tk.LEFT)
        return b

    def _button_click(self, name):
        self.trigger_tool(name)

    def toggle_toolitem(self, name, toggled):
        if name not in self._toolitems:
            return
        for toolitem in self._toolitems[name]:
            if toggled:
                toolitem.select()
            else:
                toolitem.deselect()

    def remove_toolitem(self, name):
        for toolitem in self._toolitems[name]:
            toolitem.pack_forget()
        del self._toolitems[name]
