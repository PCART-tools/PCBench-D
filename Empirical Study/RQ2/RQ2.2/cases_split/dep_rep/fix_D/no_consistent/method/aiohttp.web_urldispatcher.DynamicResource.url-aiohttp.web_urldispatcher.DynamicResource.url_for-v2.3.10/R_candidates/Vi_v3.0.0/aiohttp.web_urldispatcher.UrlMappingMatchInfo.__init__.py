    def __init__(self, match_dict, route):
        super().__init__(match_dict)
        self._route = route
        self._apps = ()
        self._current_app = None
        self._frozen = False
