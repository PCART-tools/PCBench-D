        def __init__(self, application, request, **kwargs):
            self.url_prefix = kwargs.pop('url_prefix', '')
            return tornado.web.RequestHandler.__init__(self, application,
                                                       request, **kwargs)
