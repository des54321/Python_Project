def range_dist(i):
    if i == 0:
        return range(0)
    if i > 0:
        return range(1,i)
    if i < 0:
        return range(i+1,0)


print(list(range_dist(1)))