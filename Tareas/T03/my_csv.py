def reader(file_object, delimiter=','):
    while True:
        line = file_object.readline().strip().split(delimiter)
        if line != ['']:
            yield line
        else:
            raise StopIteration
