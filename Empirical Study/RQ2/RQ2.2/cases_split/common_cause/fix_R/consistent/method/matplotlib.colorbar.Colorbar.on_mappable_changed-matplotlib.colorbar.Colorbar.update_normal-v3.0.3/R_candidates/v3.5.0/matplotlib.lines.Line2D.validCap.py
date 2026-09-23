    @_api.deprecated("3.4")
    @_api.classproperty
    def validCap(cls):
        return tuple(cs.value for cs in CapStyle)
