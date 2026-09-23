    @pytest.mark.parametrize('pickle', [True, False])
    def test_callback_complete(self, pickle):
        # ensure we start with an empty registry
        self.is_empty()

        # create a class for testing
        mini_me = Test_callback_registry()

        # test that we can add a callback
        cid1 = self.connect(self.signal, mini_me.dummy, pickle)
        assert type(cid1) is int
        self.is_not_empty()

        # test that we don't add a second callback
        cid2 = self.connect(self.signal, mini_me.dummy, pickle)
        assert cid1 == cid2
        self.is_not_empty()
        assert len(self.callbacks._func_cid_map) == 1
        assert len(self.callbacks.callbacks) == 1

        del mini_me

        # check we now have no callbacks registered
        self.is_empty()
