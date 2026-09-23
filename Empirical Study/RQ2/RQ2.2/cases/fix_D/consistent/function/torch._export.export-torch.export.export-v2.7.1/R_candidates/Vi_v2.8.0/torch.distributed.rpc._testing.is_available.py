def is_available() -> bool:
    return hasattr(torch._C, "_faulty_agent_init")
