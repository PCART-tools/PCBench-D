    class MyCallback(Callback):
        def _start(self, dsk):
            self.dsk = dsk

        def _pretask(self, key, dsk, state):
            assert key in self.dsk
