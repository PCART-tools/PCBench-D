class NavigationToolbar2Tk(NavigationToolbar2, Tk.Frame):
    """
    Attributes
    ----------
    canvas : `FigureCanvas`
        the figure canvas on which to operate
    win : tk.Window
        the tk.Window which owns this toolbar

    """
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.window = window
        NavigationToolbar2.__init__(self, canvas)

    def destroy(self, *args):
        del self.message
        Tk.Frame.destroy(self, *args)

    def set_message(self, s):
        self.message.set(s)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y0 = height - y0
        y1 = height - y1
        if hasattr(self, "lastrect"):
            self.canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.canvas._tkcanvas.create_rectangle(x0, y0, x1, y1)

        #self.canvas.draw()

    def release(self, event):
        try: self.lastrect
        except AttributeError: pass
        else:
            self.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect

    def set_cursor(self, cursor):
        self.window.configure(cursor=cursord[cursor])
        self.window.update_idletasks()

    def _Button(self, text, file, command, extension='.gif'):
        img_file = os.path.join(
            rcParams['datapath'], 'images', file + extension)
        im = Tk.PhotoImage(master=self, file=img_file)
        b = Tk.Button(
            master=self, text=text, padx=2, pady=2, image=im, command=command)
        b._ntimage = im
        b.pack(side=Tk.LEFT)
        return b

    def _Spacer(self):
        # Buttons are 30px high, so make this 26px tall with padding to center it
        s = Tk.Frame(
            master=self, height=26, relief=Tk.RIDGE, pady=2, bg="DarkGray")
        s.pack(side=Tk.LEFT, padx=5)
        return s

    def _init_toolbar(self):
        xmin, xmax = self.canvas.figure.bbox.intervalx
        height, width = 50, xmax-xmin
        Tk.Frame.__init__(self, master=self.window,
                          width=int(width), height=int(height),
                          borderwidth=2)

        self.update()  # Make axes menu

        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                # Add a spacer; return value is unused.
                self._Spacer()
            else:
                button = self._Button(text=text, file=image_file,
                                      command=getattr(self, callback))
                if tooltip_text is not None:
                    ToolTip.createToolTip(button, tooltip_text)

        self.message = Tk.StringVar(master=self)
        self._message_label = Tk.Label(master=self, textvariable=self.message)
        self._message_label.pack(side=Tk.RIGHT)
        self.pack(side=Tk.BOTTOM, fill=Tk.X)

    def configure_subplots(self):
        toolfig = Figure(figsize=(6,3))
        window = Tk.Toplevel()
        canvas = type(self.canvas)(toolfig, master=window)
        toolfig.subplots_adjust(top=0.9)
        canvas.tool = SubplotTool(self.canvas.figure, toolfig)
        canvas.draw()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        window.grab_set()

    def save_figure(self, *args):
        import tkinter.filedialog, tkinter.messagebox
        filetypes = self.canvas.get_supported_filetypes().copy()
        default_filetype = self.canvas.get_default_filetype()

        # Tk doesn't provide a way to choose a default filetype,
        # so we just have to put it first
        default_filetype_name = filetypes.pop(default_filetype)
        sorted_filetypes = ([(default_filetype, default_filetype_name)]
                            + sorted(filetypes.items()))
        tk_filetypes = [(name, '*.%s' % ext) for ext, name in sorted_filetypes]

        # adding a default extension seems to break the
        # asksaveasfilename dialog when you choose various save types
        # from the dropdown.  Passing in the empty string seems to
        # work - JDH!
        #defaultextension = self.canvas.get_default_filetype()
        defaultextension = ''
        initialdir = os.path.expanduser(rcParams['savefig.directory'])
        initialfile = self.canvas.get_default_filename()
        fname = tkinter.filedialog.asksaveasfilename(
            master=self.window,
            title='Save the figure',
            filetypes=tk_filetypes,
            defaultextension=defaultextension,
            initialdir=initialdir,
            initialfile=initialfile,
            )

        if fname in ["", ()]:
            return
        # Save dir for next time, unless empty str (i.e., use cwd).
        if initialdir != "":
            rcParams['savefig.directory'] = (
                os.path.dirname(str(fname)))
        try:
            # This method will handle the delegation to the correct type
            self.canvas.figure.savefig(fname)
        except Exception as e:
            tkinter.messagebox.showerror("Error saving file", str(e))

    def set_active(self, ind):
        self._ind = ind
        self._active = [self._axes[i] for i in self._ind]

    def update(self):
        self._axes = self.canvas.figure.axes
        with _restore_foreground_window_at_end():
            NavigationToolbar2.update(self)
