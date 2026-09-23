    def destroy(self, *args):
        if hasattr(self, 'toolbar') and self.toolbar is not None:
            self.toolbar.destroy()
        if hasattr(self, 'vbox'):
            self.vbox.destroy()
        if hasattr(self, 'window'):
            self.window.destroy()
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        self.__dict__.clear()   #Is this needed? Other backends don't have it.

        if Gcf.get_num_fig_managers()==0 and \
               not matplotlib.is_interactive() and \
               gtk.main_level() >= 1:
            gtk.main_quit()
