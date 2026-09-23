    def prune(self, klass):
        if self.op != "~":
            raise NotImplementedError("UnaryOp only support invert type ops")

        operand = self.operand
        operand = operand.prune(klass)

        if operand is not None and (
            issubclass(klass, ConditionBinOp)
            and operand.condition is not None
            or not issubclass(klass, ConditionBinOp)
            and issubclass(klass, FilterBinOp)
            and operand.filter is not None
        ):
            return operand.invert()
        return None
