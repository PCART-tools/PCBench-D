    def __new__(cls, fulldomain, condition):
        condition = condition.xreplace(dict((rs, rs.symbol)
            for rs in random_symbols(condition)))
        return Basic.__new__(cls, fulldomain, condition)
