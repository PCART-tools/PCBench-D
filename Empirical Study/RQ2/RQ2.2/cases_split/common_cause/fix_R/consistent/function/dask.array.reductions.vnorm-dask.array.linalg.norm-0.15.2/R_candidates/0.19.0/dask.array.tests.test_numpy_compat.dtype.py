@pytest.fixture(params=[
    [('A', ('f4', (3, 2))), ('B', ('f4', 3)), ('C', ('f8', 3))],
    [('A', ('i4', (3, 2))), ('B', ('f4', 3)), ('C', ('S4', 3))],
])
def dtype(request):
    return np.dtype(request.param)
