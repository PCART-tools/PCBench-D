    def __init__(self, name, is_local):
        if is_local:
            msg = 'local variable {0!r} is not defined'
        else:
            msg = 'name {0!r} is not defined'
        super(UndefinedVariableError, self).__init__(msg.format(name))
