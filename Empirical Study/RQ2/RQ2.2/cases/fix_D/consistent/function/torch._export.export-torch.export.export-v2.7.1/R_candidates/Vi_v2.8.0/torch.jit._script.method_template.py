        def method_template(self, *args, **kwargs):
            return self.forward_magic_method(method_name, *args, **kwargs)
