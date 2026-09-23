    def __call__(self, func):
        self.delayed_init(func)
        import nose.tools

        @nose.tools.with_setup(self.setup, self.teardown)
        def runner_wrapper():
            for case in self.nose_runner():
                yield case

        return _copy_metadata(func, runner_wrapper)
