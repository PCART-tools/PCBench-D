@_api.deprecated("3.3", alternative="Glue('ss')")
class SsGlue(Glue):
    def __init__(self):
        super().__init__('ss')
