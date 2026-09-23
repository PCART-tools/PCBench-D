    def __init__(self, text: str = None, conversation_id: UUID = None):
        if not conversation_id:
            conversation_id = uuid.uuid4()
        self.uuid: UUID = conversation_id
        self.past_user_inputs: List[str] = []
        self.generated_responses: List[str] = []
        self.history: List[int] = []
        self.new_user_input: Optional[str] = text
