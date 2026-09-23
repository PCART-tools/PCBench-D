        def print_tif(self, filename_or_obj, *args, dryrun=False,
                      pil_kwargs=None, **kwargs):
            buf, size = self.print_to_buffer()
            if dryrun:
                return
            image = Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)
            if pil_kwargs is None:
                pil_kwargs = {}
            pil_kwargs.setdefault("dpi", (self.figure.dpi, self.figure.dpi))
            return image.save(filename_or_obj, format='tiff', **pil_kwargs)
