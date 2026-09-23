        def print_tif(self, filename_or_obj, *args, **kwargs):
            buf, size = self.print_to_buffer()
            if kwargs.pop("dryrun", False):
                return
            image = Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)
            dpi = (self.figure.dpi, self.figure.dpi)
            return image.save(filename_or_obj, format='tiff',
                              dpi=dpi)
