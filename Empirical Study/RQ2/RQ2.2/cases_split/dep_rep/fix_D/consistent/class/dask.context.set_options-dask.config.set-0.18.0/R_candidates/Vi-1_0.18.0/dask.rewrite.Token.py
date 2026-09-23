class Token(object):
    """A token object.

    Used to express certain objects in the traversal of a task or pattern."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
