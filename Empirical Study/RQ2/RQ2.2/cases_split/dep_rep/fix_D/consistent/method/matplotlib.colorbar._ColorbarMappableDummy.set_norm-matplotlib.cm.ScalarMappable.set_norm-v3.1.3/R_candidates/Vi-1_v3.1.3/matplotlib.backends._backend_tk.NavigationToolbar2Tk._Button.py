    def _Button(self, text, file, command, extension='.gif'):
        img_file = os.path.join(
            rcParams['datapath'], 'images', file + extension)
        im = tk.PhotoImage(master=self, file=img_file)
        b = tk.Button(
            master=self, text=text, padx=2, pady=2, image=im, command=command)
        b._ntimage = im
        b.pack(side=tk.LEFT)
        return b
