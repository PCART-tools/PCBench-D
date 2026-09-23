    def stop_event_loop(self):
        # docstring inherited
        if self._event_loop_id:
            self._master.after_cancel(self._event_loop_id)
            self._event_loop_id = None
        self._master.quit()
