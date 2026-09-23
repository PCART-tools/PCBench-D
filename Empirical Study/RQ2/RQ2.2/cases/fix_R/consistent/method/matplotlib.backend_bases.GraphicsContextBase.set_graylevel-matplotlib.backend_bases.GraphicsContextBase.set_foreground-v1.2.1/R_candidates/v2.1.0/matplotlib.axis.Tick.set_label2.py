    def set_label2(self, s):
        """
        Set the text of ticklabel2

        ACCEPTS: str
        """
        self.label2.set_text(s)
        self.stale = True
