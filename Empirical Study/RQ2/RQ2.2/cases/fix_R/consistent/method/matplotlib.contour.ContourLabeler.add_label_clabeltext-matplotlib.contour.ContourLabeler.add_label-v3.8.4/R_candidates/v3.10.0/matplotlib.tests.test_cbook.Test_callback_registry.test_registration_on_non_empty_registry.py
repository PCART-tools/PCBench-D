    @pytest.mark.parametrize('pickle', [True, False])
    @pytest.mark.parametrize('cls', [Hashable, Unhashable])
    def test_registration_on_non_empty_registry(self, pickle, cls):
        # ensure we start with an empty registry
        self.is_empty()

        # setup the registry with a callback
        mini_me = cls()
        self.connect(self.signal, mini_me.dummy, pickle)

        # Add another callback
        mini_me2 = cls()
        self.connect(self.signal, mini_me2.dummy, pickle)

        # Remove and add the second callback
        mini_me2 = cls()
        self.connect(self.signal, mini_me2.dummy, pickle)

        # We still have 2 references
        self.is_not_empty()
        assert self.count() == 2

        # Removing the last 2 references
        mini_me = None
        mini_me2 = None
        self.is_empty()
