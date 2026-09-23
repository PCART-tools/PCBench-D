    def _supports_transparency(self):
        suffix = Path(self.outfile).suffix
        if suffix in {'.apng', '.avif', '.gif', '.webm', '.webp'}:
            return True
        # This list was found by going through `ffmpeg -codecs` for video encoders,
        # running them with _support_transparency() forced to True, and checking that
        # the "Pixel format" in Kdenlive included alpha. Note this is not a guarantee
        # that transparency will work; you may also need to pass `-pix_fmt`, but we
        # trust the user has done so if they are asking for these formats.
        return self.codec in {
            'apng', 'avrp', 'bmp', 'cfhd', 'dpx', 'ffv1', 'ffvhuff', 'gif', 'huffyuv',
            'jpeg2000', 'ljpeg', 'png', 'prores', 'prores_aw', 'prores_ks', 'qtrle',
            'rawvideo', 'targa', 'tiff', 'utvideo', 'v408', }
