def construct_instruction(instruction_list_from_yaml: List[Any]) -> str:
    instruction_list_part = []
    for instruction in instruction_list_from_yaml:
        instruction_list_part.append(
            ONE_INSTRUCTION.substitute(
                operator_name=instruction[0],
                X=instruction[1],
                N=instruction[2],
            )
        )
    return INSTRUCTION_LIST.substitute(instruction_list="".join(instruction_list_part).lstrip("\n"))
