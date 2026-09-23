    def _Button(self, text, image_file, toggle, frame):
        if image_file is not None:
            im = Tk.PhotoImage(master=self, file=image_file)
        else:
            im = None

        if not toggle:
            b = Tk.Button(master=frame, text=text, padx=2, pady=2, image=im,
                          command=lambda: self._button_click(text))
        else:
            b = Tk.Checkbutton(master=frame, text=text, padx=2, pady=2,
                               image=im, indicatoron=False,
                               command=lambda: self._button_click(text))
        b._ntimage = im
        b.pack(side=Tk.LEFT)
        return b
