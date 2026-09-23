def recenter(was: Stat, now: float) -> Stat:
    return {'center': now - was['center'], 'spread': was['spread']}
