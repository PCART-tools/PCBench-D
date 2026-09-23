    def start_event_loop(self, timeout=0):
        # docstring inherited
        if hasattr(self, '_event_loop'):
            raise RuntimeError("Event loop already running")
        timer = wx.Timer(self, id=wx.ID_ANY)
        if timeout > 0:
            timer.Start(timeout * 1000, oneShot=True)
            self.Bind(wx.EVT_TIMER, self.stop_event_loop, id=timer.GetId())
        # Event loop handler for start/stop event loop
        self._event_loop = wx.GUIEventLoop()
        self._event_loop.Run()
        timer.Stop()
