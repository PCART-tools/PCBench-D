    def _more_tags(self):
        regressor = self.regressor
        if regressor is None:
            from ..linear_model import LinearRegression

            regressor = LinearRegression()

        return {
            "poor_score": True,
            "multioutput": _safe_tags(regressor, key="multioutput"),
        }
