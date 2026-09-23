    @classmethod
    def _add_comparison_methods(cls):
        """ add in comparison methods """
        cls.__eq__ = _period_index_cmp('__eq__', cls)
        cls.__ne__ = _period_index_cmp('__ne__', cls)
        cls.__lt__ = _period_index_cmp('__lt__', cls)
        cls.__gt__ = _period_index_cmp('__gt__', cls)
        cls.__le__ = _period_index_cmp('__le__', cls)
        cls.__ge__ = _period_index_cmp('__ge__', cls)
