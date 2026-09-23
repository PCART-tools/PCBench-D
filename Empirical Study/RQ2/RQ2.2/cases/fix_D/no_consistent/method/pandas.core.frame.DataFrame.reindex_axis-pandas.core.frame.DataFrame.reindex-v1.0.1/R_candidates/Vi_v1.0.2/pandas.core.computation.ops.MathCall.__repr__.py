    def __repr__(self) -> str:
        operands = map(str, self.operands)
        return pprint_thing(f"{self.op}({','.join(operands)})")
