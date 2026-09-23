    def url_for(self, *args, **kwargs):
        raise RuntimeError(".url_for() is not allowed for SystemRoute")
