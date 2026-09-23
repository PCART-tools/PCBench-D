    @pytest.mark.parametrize('pickle', [True, False])
    def test_callback_disconnect(self, pickle):
        # ensure we start with an empty registry
        self.is_empty()

        # create a class for testing
        mini_me = Test_callback_registry()

        # test that we can add a callback
        cid1 = self.connect(self.signal, mini_me.dummy, pickle)
        assert type(cid1) == int
        self.is_not_empty()

        self.disconnect(cid1)

        # check we now have no callbacks registered
        self.is_empty()
