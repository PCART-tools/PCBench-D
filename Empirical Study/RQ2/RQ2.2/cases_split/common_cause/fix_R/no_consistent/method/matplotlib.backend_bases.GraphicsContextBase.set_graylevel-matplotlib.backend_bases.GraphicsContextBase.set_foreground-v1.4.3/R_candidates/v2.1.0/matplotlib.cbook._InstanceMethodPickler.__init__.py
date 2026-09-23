    def __init__(self, instancemethod):
        """Takes an instancemethod as its only argument."""
        if six.PY3:
            self.parent_obj = instancemethod.__self__
            self.instancemethod_name = instancemethod.__func__.__name__
        else:
            self.parent_obj = instancemethod.im_self
            self.instancemethod_name = instancemethod.im_func.__name__
