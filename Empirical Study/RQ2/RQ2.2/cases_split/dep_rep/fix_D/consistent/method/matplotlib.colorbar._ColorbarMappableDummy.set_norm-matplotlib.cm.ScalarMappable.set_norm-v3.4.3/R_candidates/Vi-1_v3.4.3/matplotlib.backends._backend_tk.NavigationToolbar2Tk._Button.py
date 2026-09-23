    def _Button(self, text, image_file, toggle, command):
        if tk.TkVersion >= 8.6:
            PhotoImage = tk.PhotoImage
        else:
            from PIL.ImageTk import PhotoImage
        image = (PhotoImage(master=self, file=image_file)
                 if image_file is not None else None)
        if not toggle:
            b = tk.Button(master=self, text=text, image=image, command=command)
        else:
            # There is a bug in tkinter included in some python 3.6 versions
            # that without this variable, produces a "visual" toggling of
            # other near checkbuttons
            # https://bugs.python.org/issue29402
            # https://bugs.python.org/issue25684
            var = tk.IntVar(master=self)
            b = tk.Checkbutton(
                master=self, text=text, image=image, command=command,
                indicatoron=False, variable=var)
            b.var = var
        b._ntimage = image
        b.pack(side=tk.LEFT)
        return b
