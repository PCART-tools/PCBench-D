    def release(self, event):
        """Button release event handler and validator"""
        if not self.ignore(event) and self.eventpress:
            event = self._clean_event(event)
            self.eventrelease = event
            self._release(event)
            self.eventpress = None
            self.eventrelease = None
            self.state.discard('move')
            return True
        return False
