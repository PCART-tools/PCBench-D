class VCentered(Vlist):
    """
    A convenience class to create a `Vlist` whose contents are
    centered within its enclosing box.
    """

    def __init__(self, elements):
        super().__init__([Glue('ss'), *elements, Glue('ss')])
