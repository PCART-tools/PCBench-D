    def check_for_ordered(self, op):
        """ assert that we are ordered """
        if not self.ordered:
            raise TypeError(
                "Categorical is not ordered for operation {op}\n"
                "you can use .as_ordered() to change the "
                "Categorical to an ordered one\n".format(op=op)
            )
