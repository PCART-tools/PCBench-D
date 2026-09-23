    def get_instancemethod(self):
        return getattr(self.parent_obj, self.instancemethod_name)
