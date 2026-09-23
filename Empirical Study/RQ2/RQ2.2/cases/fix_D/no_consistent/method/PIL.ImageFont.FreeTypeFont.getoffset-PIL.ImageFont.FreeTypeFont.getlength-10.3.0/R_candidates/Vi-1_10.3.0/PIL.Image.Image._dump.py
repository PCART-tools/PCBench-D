    def _dump(
        self, file: str | None = None, format: str | None = None, **options
    ) -> str:
        suffix = ""
        if format:
            suffix = "." + format

        if not file:
            f, filename = tempfile.mkstemp(suffix)
            os.close(f)
        else:
            filename = file
            if not filename.endswith(suffix):
                filename = filename + suffix

        self.load()

        if not format or format == "PPM":
            self.im.save_ppm(filename)
        else:
            self.save(filename, format, **options)

        return filename
