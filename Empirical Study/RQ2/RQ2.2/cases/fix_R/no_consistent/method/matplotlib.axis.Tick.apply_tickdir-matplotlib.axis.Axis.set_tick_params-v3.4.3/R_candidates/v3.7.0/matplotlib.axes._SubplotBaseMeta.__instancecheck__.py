    def __instancecheck__(self, obj):
        return (isinstance(obj, _base._AxesBase)
                and obj.get_subplotspec() is not None)
