    def print_svgz(self, filename, **kwargs):
        with cbook.open_file_cm(filename, "wb") as fh, \
                gzip.GzipFile(mode='w', fileobj=fh) as gzipwriter:
            return self.print_svg(gzipwriter, **kwargs)
