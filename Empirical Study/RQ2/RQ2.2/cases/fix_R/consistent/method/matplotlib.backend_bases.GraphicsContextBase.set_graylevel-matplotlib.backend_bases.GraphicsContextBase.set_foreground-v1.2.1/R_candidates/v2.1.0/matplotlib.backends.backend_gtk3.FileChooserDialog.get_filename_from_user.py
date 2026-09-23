    def get_filename_from_user (self):
        while True:
            filename = None
            if self.run() != int(Gtk.ResponseType.OK):
                break
            filename = self.get_filename()
            break

        return filename, self.ext
