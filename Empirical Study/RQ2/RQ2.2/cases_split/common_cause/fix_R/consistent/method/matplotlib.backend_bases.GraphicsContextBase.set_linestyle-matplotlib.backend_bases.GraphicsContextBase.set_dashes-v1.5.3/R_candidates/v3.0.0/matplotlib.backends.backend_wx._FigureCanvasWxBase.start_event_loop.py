    def start_event_loop(self, timeout=0):
        """
        Start an event loop.  This is used to start a blocking event
        loop so that interactive functions, such as ginput and
        waitforbuttonpress, can wait for events.  This should not be
        confused with the main GUI event loop, which is always running
        and has nothing to do with this.

        This call blocks until a callback function triggers
        stop_event_loop() or *timeout* is reached.  If *timeout* is
        <=0, never timeout.

        Raises RuntimeError if event loop is already running.
        """
        if hasattr(self, '_event_loop'):
            raise RuntimeError("Event loop already running")
        id = wx.NewId()
        timer = wx.Timer(self, id=id)
        if timeout > 0:
            timer.Start(timeout * 1000, oneShot=True)
            self.Bind(wx.EVT_TIMER, self.stop_event_loop, id=id)

        # Event loop handler for start/stop event loop
        self._event_loop = wx.GUIEventLoop()
        self._event_loop.Run()
        timer.Stop()
