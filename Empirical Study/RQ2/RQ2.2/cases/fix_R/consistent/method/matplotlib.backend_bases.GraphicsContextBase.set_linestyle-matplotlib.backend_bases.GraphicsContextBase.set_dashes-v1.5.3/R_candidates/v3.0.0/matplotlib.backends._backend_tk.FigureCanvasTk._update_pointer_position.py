    def _update_pointer_position(self, guiEvent=None):
        """
        Figure out if we are inside the canvas or not and update the
        canvas enter/leave events
        """
        # if the pointer if over the canvas, set the lastx and lasty
        # attrs of the canvas so it can process event w/o mouse click
        # or move

        # the window's upper, left coords in screen coords
        xw = self._tkcanvas.winfo_rootx()
        yw = self._tkcanvas.winfo_rooty()
        # the pointer's location in screen coords
        xp, yp = self._tkcanvas.winfo_pointerxy()

        # not figure out the canvas coordinates of the pointer
        xc = xp - xw
        yc = yp - yw

        # flip top/bottom
        yc = self.figure.bbox.height - yc

        # JDH: this method was written originally to get the pointer
        # location to the backend lastx and lasty attrs so that events
        # like KeyEvent can be handled without mouse events.  e.g., if
        # the cursor is already above the axes, then key presses like
        # 'g' should toggle the grid.  In order for this to work in
        # backend_bases, the canvas needs to know _lastx and _lasty.
        # There are three ways to get this info the canvas:
        #
        # 1) set it explicitly
        #
        # 2) call enter/leave events explicitly.  The downside of this
        #    in the impl below is that enter could be repeatedly
        #    triggered if the mouse is over the axes and one is
        #    resizing with the keyboard.  This is not entirely bad,
        #    because the mouse position relative to the canvas is
        #    changing, but it may be surprising to get repeated entries
        #    without leaves
        #
        # 3) process it as a motion notify event.  This also has pros
        #    and cons.  The mouse is moving relative to the window, but
        #    this may surpise an event handler writer who is getting
        #   motion_notify_events even if the mouse has not moved

        # here are the three scenarios
        if 1:
            # just manually set it
            self._lastx, self._lasty = xc, yc
        elif 0:
            # alternate implementation: process it as a motion
            FigureCanvasBase.motion_notify_event(self, xc, yc, guiEvent)
        elif 0:
            # alternate implementation -- process enter/leave events
            # instead of motion/notify
            if self.figure.bbox.contains(xc, yc):
                self.enter_notify_event(guiEvent, xy=(xc,yc))
            else:
                self.leave_notify_event(guiEvent)
