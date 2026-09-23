    def __init__(
            self, *,
            name: str,
            type_: Type,
            alias: str=None,
            class_validators: List[Validator]=None,
            default: Any=None,
            required: bool=False,
            allow_none: bool=False,
            model_config: Any=None,
            description: str=None):

        self.name: str = name
        self.alias: str = alias or name
        self.type_: type = type_
        self.key_type_: type = None
        class_validators = class_validators or []
        self.validate_always: bool = (
            getattr(self.type_, 'validate_always', False) or any(v.always for v in class_validators)
        )
        self.sub_fields: List[Field] = None
        self.key_field: Field = None
        self.validators = []
        self.whole_pre_validators = None
        self.whole_post_validators = None
        self.default: Any = default
        self.required: bool = required
        self.model_config = model_config
        self.description: str = description
        self.allow_none: bool = allow_none
        self.shape: Shape = Shape.SINGLETON
        self.info = {}
        self._prepare(class_validators)
