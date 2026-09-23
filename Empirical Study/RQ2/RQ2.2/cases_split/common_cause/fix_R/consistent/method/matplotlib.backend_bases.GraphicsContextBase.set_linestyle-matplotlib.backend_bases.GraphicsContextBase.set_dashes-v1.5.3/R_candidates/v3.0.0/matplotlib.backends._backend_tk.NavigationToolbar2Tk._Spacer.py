    def _Spacer(self):
        # Buttons are 30px high, so make this 26px tall with padding to center it
        s = Tk.Frame(
            master=self, height=26, relief=Tk.RIDGE, pady=2, bg="DarkGray")
        s.pack(side=Tk.LEFT, padx=5)
        return s
