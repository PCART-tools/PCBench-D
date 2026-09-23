    def prune(self, klass):

        if self.op != '~':
            raise NotImplementedError("UnaryOp only support invert type ops")

        operand = self.operand
        operand = operand.prune(klass)

        if operand is not None:
            if issubclass(klass, ConditionBinOp):
                if operand.condition is not None:
                    return operand.invert()
            elif issubclass(klass, FilterBinOp):
                if operand.filter is not None:
                    return operand.invert()

        return None
