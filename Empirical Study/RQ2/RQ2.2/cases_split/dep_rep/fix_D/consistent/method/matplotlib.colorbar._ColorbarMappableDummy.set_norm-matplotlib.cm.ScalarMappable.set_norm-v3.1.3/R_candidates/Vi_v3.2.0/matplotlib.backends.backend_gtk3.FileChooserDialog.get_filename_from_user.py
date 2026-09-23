    def get_filename_from_user(self):
        if self.run() == int(Gtk.ResponseType.OK):
            return self.get_filename(), self.ext
        else:
            return None, self.ext
