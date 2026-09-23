def is_available():
    return hasattr(torch._C, "_faulty_agent_init")
