def medium_transpose():
    return (
        rand(32, 12, 64, 64).transpose(-1, -2),
        rand(32, 12, 64, 64).transpose(-1, -2),
    )
