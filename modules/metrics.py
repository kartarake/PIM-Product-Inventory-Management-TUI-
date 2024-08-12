import shops

def timeperiod(con, lwshop):
    data = shops.fetchchanges(con, lwshop)
    firstrow = data[0]
    lastrow = data[-1]

    start = str(firstrow[2])
    end = str(lastrow[2])

    start = int(start[0:4])*365 + int(start[5:7])*30 + int(start[8:10])
    end = int(end[0:4])*365 + int(end[5:7])*30 + int(end[8:10])

    timeperiod = end - start
    return timeperiod