    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        use_returning_into = self.settings_dict["OPTIONS"].get('use_returning_into', True)
        self.features.can_return_id_from_insert = use_returning_into
