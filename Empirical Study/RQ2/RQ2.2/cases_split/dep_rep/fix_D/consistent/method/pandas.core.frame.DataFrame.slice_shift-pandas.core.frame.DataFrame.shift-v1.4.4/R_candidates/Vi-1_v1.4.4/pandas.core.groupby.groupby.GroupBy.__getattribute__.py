    def __getattribute__(self, attr: str):
        # Intercept nth to allow both call and index
        if attr == "nth":
            return GroupByNthSelector(self)
        elif attr == "nth_actual":
            return super().__getattribute__("nth")
        else:
            return super().__getattribute__(attr)
