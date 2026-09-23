    def __init__(self, config):
        super().__init__(config)

        self.mobilebert = MobileBertModel(config)
        self.cls = MobileBertOnlyNSPHead(config)

        self.init_weights()
