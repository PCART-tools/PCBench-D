def render_tests(testcases: List[TestCase]) -> None:  # type: ignore[no-any-unimported]
    num_passed = 0
    num_skipped = 0
    num_failed = 0
    for testcase in testcases:
        if not testcase.result:
            num_passed += 1
            continue
        for result in testcase.result:
            if isinstance(result, Error):
                icon = ":rotating_light: [white on red]ERROR[/white on red]:"
                num_failed += 1
            elif isinstance(result, Failure):
                icon = ":x: [white on red]Failure[/white on red]:"
                num_failed += 1
            else:
                num_skipped += 1
                continue
            rich.print(f"{icon} [bold red]{testcase.classname}.{testcase.name}[/bold red]")
            print(f"{result.text}")
    rich.print(f":white_check_mark: {num_passed} [green]Passed[green]")
    rich.print(f":dash: {num_skipped} [grey]Skipped[grey]")
    rich.print(f":rotating_light: {num_failed} [grey]Failed[grey]")
