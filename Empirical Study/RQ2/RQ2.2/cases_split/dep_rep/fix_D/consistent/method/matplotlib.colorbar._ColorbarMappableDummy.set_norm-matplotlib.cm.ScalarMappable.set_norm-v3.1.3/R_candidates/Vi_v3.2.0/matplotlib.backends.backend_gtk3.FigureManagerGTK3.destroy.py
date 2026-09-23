    def destroy(self, *args):
        self.vbox.destroy()
        self.window.destroy()
        self.canvas.destroy()
        if self.toolbar:
            self.toolbar.destroy()

        if (Gcf.get_num_fig_managers() == 0 and
                not matplotlib.is_interactive() and
                Gtk.main_level() >= 1):
            Gtk.main_quit()
