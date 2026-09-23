def command_line_usage() -> None:
    if len(sys.argv) < 2:
        print("Usage: python bisect_update.py <start|end|good|bad>")
        sys.exit(1)

    bisection_manager = CompilerBisector()
    command = sys.argv[1]

    if command == "end":
        bisection_manager.delete_bisect_status()
        sys.exit(0)

    if command == "start":
        bisection_manager.delete_bisect_status()
        bisection_manager.initialize_system()
        sys.exit(0)

    if command not in ["good", "bad"]:
        print("Invalid command. Must be 'good', 'bad', 'start', or 'end'.")
        sys.exit(1)

    def test_function() -> bool:
        return command == "good"

    if not bisection_manager.get_backend():
        raise ValueError("Must call start prior to good or bad")

    bisection_manager.do_bisect(test_function, cli_interface=True)
