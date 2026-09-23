    def __init__(self):
        self.existing_entries = {}  # object ID => (offset, generation)
        self.new_entries = {}  # object ID => (offset, generation)
        self.deleted_entries = {0: 65536}  # object ID => generation
        self.reading_finished = False
