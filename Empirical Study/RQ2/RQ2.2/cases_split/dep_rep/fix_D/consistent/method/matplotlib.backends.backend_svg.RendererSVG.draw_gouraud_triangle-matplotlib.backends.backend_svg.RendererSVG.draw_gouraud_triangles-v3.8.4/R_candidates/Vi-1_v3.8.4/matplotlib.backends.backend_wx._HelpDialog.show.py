    @classmethod
    def show(cls, parent, help_entries):
        # if no dialog is shown, create one; otherwise just re-raise it
        if cls._instance:
            cls._instance.Raise()
            return
        cls._instance = cls(parent, help_entries)
        cls._instance.Show()
