def _detect_and_normalize_assert_statement(
    self: "InstructionTranslatorBase",
    truth_fn: typing.Callable[[object], bool],
    push: bool,
):
    # Detect if this jump instruction is assert and normalize the assert
    # by pushing dummy error message when nothing is given.
    #
    # Python 3.9 assertion is in following format:
    # 18 POP_JUMP_IF_TRUE       28
    # 20 LOAD_ASSERTION_ERROR
    # 22 LOAD_CONST               3 ('Assert message') -> optional instruction
    # 24 CALL_FUNCTION            1                    -> optional instruction
    # 26 RAISE_VARARGS
    #
    # Python 3.8 assertion is in following format:
    # 18 POP_JUMP_IF_TRUE       28
    # 20 LOAD_GLOBAL              0 (Assertion type)
    # 22 LOAD_CONST               3 ('Assert message') -> optional instruction
    # 24 CALL_FUNCTION            1                    -> optional instruction
    # 26 RAISE_VARARGS            1

    if (truth_fn is not operator.truth) or push:
        return False

    assert isinstance(self.instruction_pointer, int)
    current_instruction_pointer = self.instruction_pointer
    inst = self.instructions[current_instruction_pointer]
    # Detect LOAD_ASSERTION_ERROR or LOAD_GLOBAL 0
    if inst.opname != "LOAD_ASSERTION_ERROR":
        return False

    current_instruction_pointer += 1

    # Use dummy error message if its hard to extract
    error_msg = "assertion error"

    inst = self.instructions[current_instruction_pointer]
    # DETECT RAISE_VARARGS or LOAD CONST
    if inst.opname == "LOAD_CONST":
        if not isinstance(inst.argval, str):
            return False
        error_msg = inst.argval

        # if it is LOAD_CONSTANT, it must be followed by CALL_FUNCTION
        # (PRECALL for Python 3.11, CALL for Python 3.12+)
        current_instruction_pointer += 1
        inst = self.instructions[current_instruction_pointer]
        if inst.opname not in ("CALL_FUNCTION", "PRECALL", "CALL"):
            return False

        # for Python 3.11, PRECALL should be followed by CALL, then RAISE_VARARGS
        # for Python != 3.11, CALL_FUNCTION/CALL should be followed by RAISE_VARARGS
        current_instruction_pointer += 1
        if inst.opname == "PRECALL":
            current_instruction_pointer += 1
        inst = self.instructions[current_instruction_pointer]

    if inst.opname != "RAISE_VARARGS":
        return False

    self.push(ConstantVariable.create(error_msg))

    return True
