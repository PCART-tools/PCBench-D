    @property
    def asi8(self):
        # do not cache or you'll create a memory leak
        return self.values.view('i8')
