    def _make_fail(name):
        def fail(self, *args, **kwargs):
            raise RuntimeError(name + " is not supported on ScriptModules")

        return fail
