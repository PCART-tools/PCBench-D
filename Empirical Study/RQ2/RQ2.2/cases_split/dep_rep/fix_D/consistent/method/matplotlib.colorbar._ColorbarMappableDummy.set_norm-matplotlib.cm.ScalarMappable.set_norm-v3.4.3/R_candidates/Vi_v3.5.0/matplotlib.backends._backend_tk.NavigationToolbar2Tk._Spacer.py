    def _Spacer(self):
        # Buttons are also 18pt high.
        s = tk.Frame(master=self, height='18p', relief=tk.RIDGE, bg='DarkGray')
        s.pack(side=tk.LEFT, padx='3p')
        return s
