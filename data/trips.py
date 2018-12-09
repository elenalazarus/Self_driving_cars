class Trip:
    def __init__(self, id, start_x, start_y, finish_x, finish_y, earliest, latest):
        self.id = id
        self.start_x = int(start_x)
        self.start_y = int(start_y)
        self.finish_x = int(finish_x)
        self.finish_y = int(finish_y)
        self.earliest = int(earliest)
        self.latest = int(latest)
        self.car = None
        self.score = 0

    def __str__(self):
        return '[{}] from {},{} to {},{}'.format(self.id, self.start_x,
                                                 self.start_y, self.finish_x,
                                                 self.finish_y)
