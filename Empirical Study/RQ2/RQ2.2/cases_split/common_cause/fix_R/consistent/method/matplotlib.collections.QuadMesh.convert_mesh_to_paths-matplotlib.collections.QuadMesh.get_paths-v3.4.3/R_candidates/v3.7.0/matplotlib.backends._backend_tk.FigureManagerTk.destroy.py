    def destroy(self, *args):
        if self.canvas._idle_draw_id:
            self.canvas._tkcanvas.after_cancel(self.canvas._idle_draw_id)
        if self.canvas._event_loop_id:
            self.canvas._tkcanvas.after_cancel(self.canvas._event_loop_id)
        if self._window_dpi_cbname:
            self._window_dpi.trace_remove('write', self._window_dpi_cbname)

        # NOTE: events need to be flushed before issuing destroy (GH #9956),
        # however, self.window.update() can break user code. An async callback
        # is the safest way to achieve a complete draining of the event queue,
        # but it leaks if no tk event loop is running. Therefore we explicitly
        # check for an event loop and choose our best guess.
        def delayed_destroy():
            self.window.destroy()

            if self._owns_mainloop and not Gcf.get_num_fig_managers():
                self.window.quit()

        if cbook._get_running_interactive_framework() == "tk":
            # "after idle after 0" avoids Tcl error/race (GH #19940)
            self.window.after_idle(self.window.after, 0, delayed_destroy)
        else:
            self.window.update()
            delayed_destroy()
