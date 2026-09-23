    def __init__(self, writer, *, use_mask=False, random=random.Random()):
        self.writer = writer
        self.use_mask = use_mask
        self.randrange = random.randrange
