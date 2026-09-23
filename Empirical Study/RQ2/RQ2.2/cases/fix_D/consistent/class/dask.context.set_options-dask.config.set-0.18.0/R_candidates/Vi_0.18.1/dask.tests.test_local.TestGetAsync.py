class TestGetAsync(GetFunctionTestMixin):
    get = staticmethod(get_sync)

    def test_get_sync_num_workers(self):
        self.get({'x': (inc, 'y'), 'y': 1}, 'x', num_workers=2)
