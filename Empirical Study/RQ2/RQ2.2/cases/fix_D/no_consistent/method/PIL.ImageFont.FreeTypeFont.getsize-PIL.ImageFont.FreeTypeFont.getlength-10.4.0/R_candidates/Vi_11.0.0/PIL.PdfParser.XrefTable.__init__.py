    def __init__(self) -> None:
        self.existing_entries: dict[int, tuple[int, int]] = (
            {}
        )  # object ID => (offset, generation)
        self.new_entries: dict[int, tuple[int, int]] = (
            {}
        )  # object ID => (offset, generation)
        self.deleted_entries = {0: 65536}  # object ID => generation
        self.reading_finished = False
