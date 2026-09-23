    def __call__(self, env):
        operand = self.operand(env)
        return self.func(operand)
