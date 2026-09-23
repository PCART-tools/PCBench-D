def parse_segments(raw_segments: List[List[int]]) -> List[LlvmCoverageSegment]:
    """
    Creates LlvmCoverageSegment from a list of lists in llvm export json.
    each segment is represented by 5-element array.
    """
    ret: List[LlvmCoverageSegment] = []
    for raw_segment in raw_segments:
        assert (
            len(raw_segment) == 5 or len(raw_segment) == 6
        ), "list is not compatible with llvmcom export:"
        " Expected to have 5 or 6 elements"
        if len(raw_segment) == 5:
            ret.append(
                LlvmCoverageSegment(
                    raw_segment[0],
                    raw_segment[1],
                    raw_segment[2],
                    raw_segment[3],
                    raw_segment[4],
                    None,
                )
            )
        else:
            ret.append(LlvmCoverageSegment(*raw_segment))

    return ret
