    def destroy(self, *args):
        if self.canvas._idle_callback:
            self.canvas._tkcanvas.after_cancel(self.canvas._idle_callback)
        if self.canvas._event_loop_id:
            self.canvas._tkcanvas.after_cancel(self.canvas._event_loop_id)

        # NOTE: events need to be flushed before issuing destroy (GH #9956),
        # however, self.window.update() can break user code. This is the
        # safest way to achieve a complete draining of the event queue,
        # but it may require users to update() on their own to execute the
        # completion in obscure corner cases.
        def delayed_destroy():
            self.window.destroy()

            if self._owns_mainloop and not Gcf.get_num_fig_managers():
                self.window.quit()

        # "after idle after 0" avoids Tcl error/race (GH #19940)
        self.window.after_idle(self.window.after, 0, delayed_destroy)
