    def _register(func):
        os.register_at_fork(after_in_child=func)
