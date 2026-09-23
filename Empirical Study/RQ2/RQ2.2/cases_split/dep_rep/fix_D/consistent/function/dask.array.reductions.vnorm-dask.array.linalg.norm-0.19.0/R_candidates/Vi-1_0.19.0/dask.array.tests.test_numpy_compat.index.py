@pytest.fixture(params=[
    ['A'],
    ['A', 'B'],
    ['A', 'B', 'C'],
])
def index(request):
    return request.param
