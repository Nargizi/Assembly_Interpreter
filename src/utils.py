def read_file(file):
    with open(file) as f:
        for line in f:
            yield line
