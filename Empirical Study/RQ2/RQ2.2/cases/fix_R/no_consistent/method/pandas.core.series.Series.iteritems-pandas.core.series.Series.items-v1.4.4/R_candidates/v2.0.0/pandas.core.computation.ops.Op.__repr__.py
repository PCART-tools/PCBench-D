    def __repr__(self) -> str:
        """
        Print a generic n-ary operator and its operands using infix notation.
        """
        # recurse over the operands
        parened = (f"({pprint_thing(opr)})" for opr in self.operands)
        return pprint_thing(f" {self.op} ".join(parened))
