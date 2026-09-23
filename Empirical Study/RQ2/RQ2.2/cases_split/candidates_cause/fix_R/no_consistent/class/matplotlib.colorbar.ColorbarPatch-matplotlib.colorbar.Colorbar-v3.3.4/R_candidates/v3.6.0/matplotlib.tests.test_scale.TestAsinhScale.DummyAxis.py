        class DummyAxis:
            def __init__(self):
                self.fields = {}
            def set(self, **kwargs):
                self.fields.update(**kwargs)
            def set_major_formatter(self, f):
                self.fields['major_formatter'] = f
