class SubSuperCluster(Hlist):
    """
    A hack to get around that fact that this code does a two-pass parse like
    TeX.  This lets us store enough information in the hlist itself, namely the
    nucleus, sub- and super-script, such that if another script follows that
    needs to be attached, it can be reconfigured on the fly.
    """

    def __init__(self):
        self.nucleus = None
        self.sub = None
        self.super = None
        super().__init__([])
