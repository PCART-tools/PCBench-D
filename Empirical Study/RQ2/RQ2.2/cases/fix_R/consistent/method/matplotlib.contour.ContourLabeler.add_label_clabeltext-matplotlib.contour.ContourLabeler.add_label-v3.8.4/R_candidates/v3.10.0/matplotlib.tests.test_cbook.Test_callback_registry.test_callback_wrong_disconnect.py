    @pytest.mark.parametrize('pickle', [True, False])
    @pytest.mark.parametrize('cls', [Hashable, Unhashable])
    def test_callback_wrong_disconnect(self, pickle, cls):
        # ensure we start with an empty registry
        self.is_empty()

        # create a class for testing
        mini_me = cls()

        # test that we can add a callback
        cid1 = self.connect(self.signal, mini_me.dummy, pickle)
        assert type(cid1) is int
        self.is_not_empty()

        self.disconnect("foo")

        # check we still have callbacks registered
        self.is_not_empty()
