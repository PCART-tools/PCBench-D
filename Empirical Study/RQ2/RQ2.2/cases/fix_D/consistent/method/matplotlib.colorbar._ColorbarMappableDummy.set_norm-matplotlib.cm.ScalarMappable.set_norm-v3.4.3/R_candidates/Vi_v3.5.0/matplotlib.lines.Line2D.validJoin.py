    @_api.deprecated("3.4")
    @_api.classproperty
    def validJoin(cls):
        return tuple(js.value for js in JoinStyle)
