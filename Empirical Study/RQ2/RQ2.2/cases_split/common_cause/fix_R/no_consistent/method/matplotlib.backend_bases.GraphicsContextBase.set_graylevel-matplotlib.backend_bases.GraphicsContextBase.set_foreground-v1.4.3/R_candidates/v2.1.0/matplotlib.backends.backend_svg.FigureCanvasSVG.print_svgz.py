    def print_svgz(self, filename, *args, **kwargs):
        if isinstance(filename, six.string_types):
            options = dict(filename=filename)
        elif is_writable_file_like(filename):
            options = dict(fileobj=filename)
        else:
            raise ValueError("filename must be a path or a file-like object")

        with gzip.GzipFile(mode='w', **options) as gzipwriter:
            return self.print_svg(gzipwriter)
