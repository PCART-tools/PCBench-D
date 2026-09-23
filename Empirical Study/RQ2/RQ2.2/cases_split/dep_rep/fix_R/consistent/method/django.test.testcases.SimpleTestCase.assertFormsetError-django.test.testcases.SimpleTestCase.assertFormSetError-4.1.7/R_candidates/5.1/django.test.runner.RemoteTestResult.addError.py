    def addError(self, test, err):
        self.check_picklable(test, err)
        self.events.append(("addError", self.test_index, err))
        super().addError(test, err)
