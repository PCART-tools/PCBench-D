    def __init__(self, elements: list[Node]):
        super().__init__([Glue('ss'), *elements, Glue('ss')], do_kern=False)
