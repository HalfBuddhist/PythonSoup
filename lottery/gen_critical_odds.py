small = 1.0

while small < 2.0:
    small += 0.01
    big = small/(small-1.0)
    print("%.2f\t%.2f" % (small, big))
