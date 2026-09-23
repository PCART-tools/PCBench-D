def main():
    initializer_parameter_map = {}
    for initializer in INITIALIZERS.keys():
        sys.stderr.write('Evaluating {} ...\n'.format(initializer))
        initializer_parameter_map[initializer] = run(initializer)

    emit(initializer_parameter_map)
