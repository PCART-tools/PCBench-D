    def __init__(self, elements):
        Hlist.__init__(self, [SsGlue()] + elements + [SsGlue()],
                       do_kern=False)
