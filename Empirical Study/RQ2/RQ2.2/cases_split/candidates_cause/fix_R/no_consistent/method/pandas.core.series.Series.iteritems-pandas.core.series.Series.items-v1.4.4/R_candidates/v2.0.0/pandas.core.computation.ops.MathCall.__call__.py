    def __call__(self, env):
        # error: "Op" not callable
        operands = [op(env) for op in self.operands]  # type: ignore[operator]
        with np.errstate(all="ignore"):
            return self.func.func(*operands)
