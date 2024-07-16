import math

def fillspace(length, string):
    got = len(string)
    need = length
    fill = need - got

    del got, need
    return fill
    
def splitspace(length, string):
    got = len(string)
    fill = length - got

    half = fill / 2
    split1 = math.ceil(half)
    split2 = math.floor(half)

    return (split1, split2)
        

def boxify(string, width = None, align = "left"):
    linelist = string.split('\n')
    maxcharinline = len(max(linelist, key=len))

    if not(width == None):
        width = width
    else:
        width = maxcharinline + 4

    belt = list()
    
    topline = '.' + ('-' * (width - 2)) + '.'
    belt.append(topline)

    if align in ("left", "l"):
        for line in linelist:
            bwline = '| ' + line + (' ' * fillspace(width - 4, line)) + ' |'
            belt.append(bwline)

    elif align in ("right", "r"):
        for line in linelist:
            bwline = '| ' + (' ' * fillspace(width - 4, line)) + line + ' |'
            belt.append(bwline)

    elif align in ("centre", "center", "c"):
        for line in linelist:
            bwline = '| ' + (' ' * splitspace(width - 4, line)[0]) + line + (' ' * splitspace(width - 4, line)[1]) + ' |'
            belt.append(bwline)

    else:
        raise ValueError('Invalid align method is passed.')

    bottomline = "'" + ('-' * (width - 2)) + "'"
    belt.append(bottomline)

    final = '\n'.join(belt)
    return final