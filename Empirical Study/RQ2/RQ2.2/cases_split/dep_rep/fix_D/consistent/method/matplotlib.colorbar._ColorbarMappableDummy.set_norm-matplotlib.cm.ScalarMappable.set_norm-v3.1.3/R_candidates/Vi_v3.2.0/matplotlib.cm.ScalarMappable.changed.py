    def changed(self):
        """
        Call this whenever the mappable is changed to notify all the
        callbackSM listeners to the 'changed' signal
        """
        self.callbacksSM.process('changed', self)

        for key in self.update_dict:
            self.update_dict[key] = True
        self.stale = True
