    def print_figure(self, *args, **kwargs):
        super().print_figure(*args, **kwargs)
        # In some cases, Qt will itself trigger a paint event after closing the file
        # save dialog. When that happens, we need to be sure that the internal canvas is
        # re-drawn. However, if the user is using an automatically-chosen Qt backend but
        # saving with a different backend (such as pgf), we do not want to trigger a
        # full draw in Qt, so just set the flag for next time.
        self._draw_pending = True
