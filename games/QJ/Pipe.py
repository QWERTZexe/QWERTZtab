class Pipe:
    def __init__(self, x, height, gap, type='normal'):
        self.x = x
        self.height = height
        self.gap = gap
        self.width = 80
        self.type = type
        self.passed = False
        self.length = self.width if type != 'tunnel' else self.width * 2 + 300