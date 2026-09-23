    def _read_dpi_from_exif(self) -> None:
        # If DPI isn't in JPEG header, fetch from EXIF
        if "dpi" in self.info or "exif" not in self.info:
            return
        try:
            exif = self.getexif()
            resolution_unit = exif[0x0128]
            x_resolution = exif[0x011A]
            try:
                dpi = float(x_resolution[0]) / x_resolution[1]
            except TypeError:
                dpi = x_resolution
            if math.isnan(dpi):
                msg = "DPI is not a number"
                raise ValueError(msg)
            if resolution_unit == 3:  # cm
                # 1 dpcm = 2.54 dpi
                dpi *= 2.54
            self.info["dpi"] = dpi, dpi
        except (
            struct.error,  # truncated EXIF
            KeyError,  # dpi not included
            SyntaxError,  # invalid/unreadable EXIF
            TypeError,  # dpi is an invalid float
            ValueError,  # dpi is an invalid float
            ZeroDivisionError,  # invalid dpi rational value
        ):
            self.info["dpi"] = 72, 72
