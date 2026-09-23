    def __call__(self, env) -> MathCall:
        operand = self.operand(env)
        # error: Cannot call function of unknown type
        return self.func(operand)  # type: ignore[operator]
