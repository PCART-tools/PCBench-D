    def __init__(self, name: str, is_local: bool | None = None):
        base_msg = f"{repr(name)} is not defined"
        if is_local:
            msg = f"local variable {base_msg}"
        else:
            msg = f"name {base_msg}"
        super().__init__(msg)
