    def __init__(self, level, global_dict=None, local_dict=None,
                 queryables=None):
        super(Scope, self).__init__(level + 1, global_dict=global_dict,
                                    local_dict=local_dict)
        self.queryables = queryables or dict()
