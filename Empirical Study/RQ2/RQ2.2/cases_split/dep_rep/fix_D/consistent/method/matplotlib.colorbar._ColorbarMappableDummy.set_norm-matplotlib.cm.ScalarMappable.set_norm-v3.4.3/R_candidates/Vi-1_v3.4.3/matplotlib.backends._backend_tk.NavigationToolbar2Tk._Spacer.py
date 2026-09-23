    def _Spacer(self):
        # Buttons are 30px high. Make this 26px tall +2px padding to center it.
        s = tk.Frame(
            master=self, height=26, relief=tk.RIDGE, pady=2, bg="DarkGray")
        s.pack(side=tk.LEFT, padx=5)
        return s
