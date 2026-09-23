    def __init__(self):
        assert _has_comet, "CometCallback requires comet-ml to be installed. Run `pip install comet-ml`."
        self._initialized = False
