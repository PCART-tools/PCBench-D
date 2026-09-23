def render_code_state(cs: defaultdict[CodeId, CodeState]) -> str:
    return "\n".join(
        f"{k.filename}:{k.firstlineno}:{k.name}:\n"
        + "\n".join(
            f"  {src}: {fs.render()}" for src, fs in v.automatic_dynamic.items()
        )
        for k, v in cs.items()
    )
