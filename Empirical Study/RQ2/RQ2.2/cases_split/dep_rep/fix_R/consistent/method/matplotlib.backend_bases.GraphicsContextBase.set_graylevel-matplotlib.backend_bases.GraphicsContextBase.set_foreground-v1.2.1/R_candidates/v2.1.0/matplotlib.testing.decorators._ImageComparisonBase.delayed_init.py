    def delayed_init(self, func):
        assert self.func is None, "it looks like same decorator used twice"
        self.func = func
        self.baseline_dir, self.result_dir = _image_directories(func)
