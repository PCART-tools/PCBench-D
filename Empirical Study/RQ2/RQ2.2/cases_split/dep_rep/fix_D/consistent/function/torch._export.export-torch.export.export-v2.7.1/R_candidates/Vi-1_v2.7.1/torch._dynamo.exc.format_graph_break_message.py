def format_graph_break_message(
    gb_type: str,
    context: str,
    explanation: str,
    hints: list[str],
) -> str:
    explanation = textwrap.indent(explanation, "    ").lstrip()
    hints_str = "\n".join(
        "  Hint: " + textwrap.indent(hint, "    ").lstrip() for hint in hints
    )
    context = textwrap.indent(context, "    ").lstrip()

    msg = f"""\
{gb_type}
  Explanation: {explanation}
{hints_str}

  Developer debug context: {context}
"""
    return msg
