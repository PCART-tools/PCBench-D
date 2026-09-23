class Test_callback_registry:
    def setup(self):
        self.signal = 'test'
        self.callbacks = cbook.CallbackRegistry()

    def connect(self, s, func, pickle):
        cid = self.callbacks.connect(s, func)
        if pickle:
            self.callbacks._pickled_cids.add(cid)
        return cid

    def disconnect(self, cid):
        return self.callbacks.disconnect(cid)

    def count(self):
        count1 = len(self.callbacks._func_cid_map.get(self.signal, []))
        count2 = len(self.callbacks.callbacks.get(self.signal))
        assert count1 == count2
        return count1

    def is_empty(self):
        np.testing.break_cycles()
        assert self.callbacks._func_cid_map == {}
        assert self.callbacks.callbacks == {}
        assert self.callbacks._pickled_cids == set()

    def is_not_empty(self):
        np.testing.break_cycles()
        assert self.callbacks._func_cid_map != {}
        assert self.callbacks.callbacks != {}

    @pytest.mark.parametrize('pickle', [True, False])
    def test_callback_complete(self, pickle):
        # ensure we start with an empty registry
        self.is_empty()

        # create a class for testing
        mini_me = Test_callback_registry()

        # test that we can add a callback
        cid1 = self.connect(self.signal, mini_me.dummy, pickle)
        assert type(cid1) == int
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

    @pytest.mark.parametrize('pickle', [True, False])
    def test_callback_wrong_disconnect(self, pickle):
        # ensure we start with an empty registry
        self.is_empty()

        # create a class for testing
        mini_me = Test_callback_registry()

        # test that we can add a callback
        cid1 = self.connect(self.signal, mini_me.dummy, pickle)
        assert type(cid1) == int
        self.is_not_empty()

        self.disconnect("foo")

        # check we still have callbacks registered
        self.is_not_empty()

    @pytest.mark.parametrize('pickle', [True, False])
    def test_registration_on_non_empty_registry(self, pickle):
        # ensure we start with an empty registry
        self.is_empty()

        # setup the registry with a callback
        mini_me = Test_callback_registry()
        self.connect(self.signal, mini_me.dummy, pickle)

        # Add another callback
        mini_me2 = Test_callback_registry()
        self.connect(self.signal, mini_me2.dummy, pickle)

        # Remove and add the second callback
        mini_me2 = Test_callback_registry()
        self.connect(self.signal, mini_me2.dummy, pickle)

        # We still have 2 references
        self.is_not_empty()
        assert self.count() == 2

        # Removing the last 2 references
        mini_me = None
        mini_me2 = None
        self.is_empty()

    def dummy(self):
        pass

    def test_pickling(self):
        assert hasattr(pickle.loads(pickle.dumps(cbook.CallbackRegistry())),
                       "callbacks")
