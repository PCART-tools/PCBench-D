def enableScriptTest():
    def script_dec(func):
        def wrapper(self):
            self.is_script_test_enabled = True
            return func(self)
        return wrapper
    return script_dec
