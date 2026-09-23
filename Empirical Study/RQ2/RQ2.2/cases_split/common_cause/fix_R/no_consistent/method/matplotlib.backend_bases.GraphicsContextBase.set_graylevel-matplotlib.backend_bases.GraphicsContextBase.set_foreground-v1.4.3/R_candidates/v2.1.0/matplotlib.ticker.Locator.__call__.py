    def __call__(self):
        """Return the locations of the ticks"""
        # note: some locators return data limits, other return view limits,
        # hence there is no *one* interface to call self.tick_values.
        raise NotImplementedError('Derived must override')
