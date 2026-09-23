def print_file_summary(
    covered_summary: int, total_summary: int, summary_file: IO[str]
) -> float:
    # print summary first
    try:
        coverage_percentage = 100.0 * covered_summary / total_summary
    except ZeroDivisionError:
        coverage_percentage = 0
    print(
        f"SUMMARY\ncovered: {covered_summary}\nuncovered: {total_summary}\npercentage: {coverage_percentage:.2f}%\n\n",
        file=summary_file,
    )
    if coverage_percentage == 0:
        print("Coverage is 0, Please check if json profiles are valid")
    return coverage_percentage
