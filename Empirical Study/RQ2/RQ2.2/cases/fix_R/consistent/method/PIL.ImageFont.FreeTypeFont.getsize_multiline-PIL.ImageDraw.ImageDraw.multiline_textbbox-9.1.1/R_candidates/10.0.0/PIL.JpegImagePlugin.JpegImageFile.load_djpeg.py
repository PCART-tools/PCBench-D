    def load_djpeg(self):
        # ALTERNATIVE: handle JPEGs via the IJG command line utilities

        f, path = tempfile.mkstemp()
        os.close(f)
        if os.path.exists(self.filename):
            subprocess.check_call(["djpeg", "-outfile", path, self.filename])
        else:
            try:
                os.unlink(path)
            except OSError:
                pass

            msg = "Invalid Filename"
            raise ValueError(msg)

        try:
            with Image.open(path) as _im:
                _im.load()
                self.im = _im.im
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass

        self.mode = self.im.mode
        self._size = self.im.size

        self.tile = []
