@pytest.mark.parametrize('err, args, kwargs, match', (
        (ValueError, (-1,), {}, r'margin must be greater than -0\.5'),
        (ValueError, (1, -1, 1), {}, r'margin must be greater than -0\.5'),
        (ValueError, (1, 1, -1), {}, r'margin must be greater than -0\.5'),
        (ValueError, tuple(), {'x': -1}, r'margin must be greater than -0\.5'),
        (ValueError, tuple(), {'y': -1}, r'margin must be greater than -0\.5'),
        (ValueError, tuple(), {'z': -1}, r'margin must be greater than -0\.5'),
        (TypeError, (1, ), {'x': 1},
         'Cannot pass both positional and keyword'),
        (TypeError, (1, ), {'x': 1, 'y': 1, 'z': 1},
         'Cannot pass both positional and keyword'),
        (TypeError, (1, ), {'x': 1, 'y': 1},
         'Cannot pass both positional and keyword'),
        (TypeError, (1, 1), {}, 'Must pass a single positional argument for'),
))
def test_margins_errors(err, args, kwargs, match):
    with pytest.raises(err, match=match):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.margins(*args, **kwargs)
