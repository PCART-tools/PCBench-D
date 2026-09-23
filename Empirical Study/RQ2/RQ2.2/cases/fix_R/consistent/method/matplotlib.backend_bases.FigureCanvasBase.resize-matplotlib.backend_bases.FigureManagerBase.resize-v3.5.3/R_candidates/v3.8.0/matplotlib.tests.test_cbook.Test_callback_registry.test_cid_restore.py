    def test_cid_restore(self):
        cb = cbook.CallbackRegistry()
        cb.connect('a', lambda: None)
        cb2 = pickle.loads(pickle.dumps(cb))
        cid = cb2.connect('c', lambda: None)
        assert cid == 1
