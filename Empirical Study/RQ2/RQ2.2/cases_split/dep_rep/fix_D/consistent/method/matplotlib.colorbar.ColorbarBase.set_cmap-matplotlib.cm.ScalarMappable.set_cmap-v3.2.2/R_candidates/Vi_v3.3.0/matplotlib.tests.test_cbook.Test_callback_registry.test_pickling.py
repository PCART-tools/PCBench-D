    def test_pickling(self):
        assert hasattr(pickle.loads(pickle.dumps(cbook.CallbackRegistry())),
                       "callbacks")
