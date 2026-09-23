    def destroy(self):
        CloseEvent("close_event", self)._process()
