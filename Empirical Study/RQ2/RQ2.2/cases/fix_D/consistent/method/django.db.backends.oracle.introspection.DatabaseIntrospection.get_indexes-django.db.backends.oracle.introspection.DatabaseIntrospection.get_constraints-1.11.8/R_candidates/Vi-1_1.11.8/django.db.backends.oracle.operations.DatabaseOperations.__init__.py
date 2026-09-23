    def __init__(self, *args, **kwargs):
        super(DatabaseOperations, self).__init__(*args, **kwargs)
        self.set_operators['difference'] = 'MINUS'
