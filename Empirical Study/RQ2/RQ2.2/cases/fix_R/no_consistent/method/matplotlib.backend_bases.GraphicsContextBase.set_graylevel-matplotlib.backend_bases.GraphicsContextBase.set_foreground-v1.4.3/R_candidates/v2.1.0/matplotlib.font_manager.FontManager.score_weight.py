    def score_weight(self, weight1, weight2):
        """
        Returns a match score between *weight1* and *weight2*.

        The result is 0.0 if both weight1 and weight 2 are given as strings
        and have the same value.

        Otherwise, the result is the absolute value of the difference between the
        CSS numeric values of *weight1* and *weight2*, normalized
        between 0.05 and 1.0.
        """

        # exact match of the weight names (e.g. weight1 == weight2 == "regular")
        if (isinstance(weight1, six.string_types) and
                isinstance(weight2, six.string_types) and
                weight1 == weight2):
            return 0.0
        try:
            weightval1 = int(weight1)
        except ValueError:
            weightval1 = weight_dict.get(weight1, 500)
        try:
            weightval2 = int(weight2)
        except ValueError:
            weightval2 = weight_dict.get(weight2, 500)
        return 0.95*(abs(weightval1 - weightval2) / 1000.0) + 0.05
