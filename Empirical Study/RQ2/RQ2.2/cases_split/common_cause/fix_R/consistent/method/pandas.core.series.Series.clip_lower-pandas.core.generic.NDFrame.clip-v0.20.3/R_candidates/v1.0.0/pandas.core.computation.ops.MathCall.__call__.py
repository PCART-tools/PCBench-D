    def __call__(self, env):
        operands = [op(env) for op in self.operands]
        with np.errstate(all="ignore"):
            return self.func.func(*operands)
