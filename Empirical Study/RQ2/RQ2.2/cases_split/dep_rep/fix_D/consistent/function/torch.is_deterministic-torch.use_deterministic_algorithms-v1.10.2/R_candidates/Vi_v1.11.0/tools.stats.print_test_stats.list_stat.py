def list_stat(l: List[float]) -> Stat:
    return {
        'center': statistics.mean(l),
        'spread': statistics.stdev(l) if len(l) > 1 else None
    }
