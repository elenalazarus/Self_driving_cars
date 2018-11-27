def reading(path):
    data = []
    with open(path, 'r') as f:
        output = f.read()
        for line in output.split('\n'):
            data.append(list(map(int, line.split())))
    data.pop(-1)
    return data