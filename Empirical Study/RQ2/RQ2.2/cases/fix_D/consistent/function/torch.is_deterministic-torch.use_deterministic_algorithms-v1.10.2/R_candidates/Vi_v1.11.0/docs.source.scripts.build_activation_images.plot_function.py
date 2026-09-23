def plot_function(function, **args):
    """
    Plot a function on the current plot. The additional arguments may
    be used to specify color, alpha, etc.
    """
    xrange = torch.arange(-7.0, 7.0, 0.01)  # We need to go beyond 6 for ReLU6
    pylab.plot(
        xrange.numpy(),
        function(xrange).detach().numpy(),
        **args
    )
