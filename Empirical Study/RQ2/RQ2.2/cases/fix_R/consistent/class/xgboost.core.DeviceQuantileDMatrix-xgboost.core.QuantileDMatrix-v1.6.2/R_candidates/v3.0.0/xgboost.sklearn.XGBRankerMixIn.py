class XGBRankerMixIn:
    """MixIn for ranking, defines the _estimator_type usually defined in scikit-learn
    base classes.

    """

    _estimator_type = "ranker"
