    def __call__(self, func):
        self.delayed_init(func)
        import nose.tools

        @functools.wraps(func)
        @nose.tools.with_setup(self.setup, self.teardown)
        def runner_wrapper():
            yield from self.nose_runner()

        return runner_wrapper
