    def set_label1(self, s):
        """
        Set the text of ticklabel

        ACCEPTS: str
        """
        self.label1.set_text(s)
        self.stale = True
