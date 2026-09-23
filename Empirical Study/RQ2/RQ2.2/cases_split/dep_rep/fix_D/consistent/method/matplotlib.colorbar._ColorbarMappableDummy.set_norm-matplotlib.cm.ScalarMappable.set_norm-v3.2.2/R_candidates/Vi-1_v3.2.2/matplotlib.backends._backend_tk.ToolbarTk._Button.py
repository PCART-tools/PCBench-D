    def _Button(self, text, image_file, toggle, frame):
        if image_file is not None:
            im = tk.PhotoImage(master=self, file=image_file)
        else:
            im = None

        if not toggle:
            b = tk.Button(master=frame, text=text, padx=2, pady=2, image=im,
                          command=lambda: self._button_click(text))
        else:
            # There is a bug in tkinter included in some python 3.6 versions
            # that without this variable, produces a "visual" toggling of
            # other near checkbuttons
            # https://bugs.python.org/issue29402
            # https://bugs.python.org/issue25684
            var = tk.IntVar()
            b = tk.Checkbutton(master=frame, text=text, padx=2, pady=2,
                               image=im, indicatoron=False,
                               command=lambda: self._button_click(text),
                               variable=var)
        b._ntimage = im
        b.pack(side=tk.LEFT)
        return b
