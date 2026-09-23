    def __call__(self, orig, dest):
        if not hasattr(self, "_tmpdir"):
            self._tmpdir = TemporaryDirectory()
            shutil.copytree(cbook._get_data_path("fonts/ttf"),
                            Path(self._tmpdir.name, "fonts"))
        return super().__call__(orig, dest)
