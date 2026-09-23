def make_attr(tx: "InstructionTranslator", name):
    node = tx.output.create_proxy(
        "get_attr",
        name,
        (),
        {},
    )
    return node
