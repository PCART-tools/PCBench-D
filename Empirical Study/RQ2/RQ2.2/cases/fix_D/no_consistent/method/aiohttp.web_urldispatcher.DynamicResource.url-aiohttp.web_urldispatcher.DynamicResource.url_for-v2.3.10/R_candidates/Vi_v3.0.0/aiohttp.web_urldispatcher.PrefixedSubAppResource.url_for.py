    def url_for(self, *args, **kwargs):
        raise RuntimeError(".url_for() is not supported "
                           "by sub-application root")
