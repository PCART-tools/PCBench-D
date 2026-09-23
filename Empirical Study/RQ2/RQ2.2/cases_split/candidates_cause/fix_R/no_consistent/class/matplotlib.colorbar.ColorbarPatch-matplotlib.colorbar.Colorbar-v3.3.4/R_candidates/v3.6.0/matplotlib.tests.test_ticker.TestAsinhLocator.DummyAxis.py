        class DummyAxis:
            bounds = (-1, 1)
            @classmethod
            def get_view_interval(cls): return cls.bounds
