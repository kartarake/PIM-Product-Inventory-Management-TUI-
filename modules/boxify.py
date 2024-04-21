import math

class stats:
    def __init__(self, string, width = None) -> None:
        self.characters = len(string) - string.count('\n')
        self.lines = string.count('\n') + 1

        self.linelist = string.split('\n')
        self.maxcharinline = len(max(self.linelist, key=len))

        if not(width == None):
            self.width = width
        else:
            self.width = self.maxcharinline + 4

        self.height = self.lines + 2

    def fillspace(self, length, string):
        got = len(string)
        need = length
        fill = need - got

        del got, need
        return fill
    
    def splitspace(self, length, string):
        got = len(string)
        fill = length - got

        half = fill / 2
        split1 = math.ceil(half)
        split2 = math.floor(half)

        return (split1, split2)
        

def boxify(string, width = None, align = "left"):
    if not(width == None):
        stat = stats(string, width = width)
    else:
        stat = stats(string)

    belt = list()
    
    topline = '.' + ('-' * (stat.width - 2)) + '.'
    belt.append(topline)

    if align in ("left", "l"):
        for line in stat.linelist:
            bwline = '| ' + line + (' ' * stat.fillspace(stat.width - 4, line)) + ' |'
            belt.append(bwline)

    elif align in ("right", "r"):
        for line in stat.linelist:
            bwline = '| ' + (' ' * stat.fillspace(stat.width - 4, line)) + line + ' |'
            belt.append(bwline)

    elif align in ("centre", "center", "c"):
        for line in stat.linelist:
            bwline = '| ' + (' ' * stat.splitspace(stat.width - 4, line)[0]) + line + (' ' * stat.splitspace(stat.width - 4, line)[1]) + ' |'
            belt.append(bwline)

    else:
        raise ValueError('Invalid align method is passed.')

    bottomline = "'" + ('-' * (stat.width - 2)) + "'"
    belt.append(bottomline)

    final = '\n'.join(belt)
    return final