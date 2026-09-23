    def get_filename_from_user (self):
        while True:
            filename = None
            if self.run() != int(gtk.RESPONSE_OK):
                break
            filename = self.get_filename()
            break

        return filename, self.ext
