    class UnexpectedButHashable:
        def __init__(self):
            self.name = "a"

        def __hash__(self):
            return hash(self.name)

        def __eq__(self, other):
            return isinstance(other, UnexpectedButHashable)
