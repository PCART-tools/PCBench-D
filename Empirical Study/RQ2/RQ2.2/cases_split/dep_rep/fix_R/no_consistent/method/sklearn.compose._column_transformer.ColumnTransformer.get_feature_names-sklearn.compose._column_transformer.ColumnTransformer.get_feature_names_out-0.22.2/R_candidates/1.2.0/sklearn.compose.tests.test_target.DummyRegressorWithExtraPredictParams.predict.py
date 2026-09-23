    def predict(self, X, check_input=True):
        # In the test below we make sure that the check input parameter is
        # passed as false
        self.predict_called = True
        assert not check_input
        return super().predict(X)
