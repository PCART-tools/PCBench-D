    def nose_runner(self):
        func = self.compare
        func = _checked_on_freetype_version(self.freetype_version)(func)
        funcs = {extension: _xfail_if_format_is_uncomparable(extension)(func)
                 for extension in self.extensions}
        for idx, baseline in enumerate(self.baseline_images):
            for extension in self.extensions:
                yield funcs[extension], idx, baseline, extension
