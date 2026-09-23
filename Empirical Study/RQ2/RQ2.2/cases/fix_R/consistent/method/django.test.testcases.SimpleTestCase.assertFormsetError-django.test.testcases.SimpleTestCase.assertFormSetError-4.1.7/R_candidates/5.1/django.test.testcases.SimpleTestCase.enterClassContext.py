        @classmethod
        def enterClassContext(cls, cm):
            return _enter_context(cm, cls.addClassCleanup)
