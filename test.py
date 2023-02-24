def read_file():
    with open("latest.log", "r") as f:
        SMRF1 = f.readlines()
    return SMRF1

initial = read_file()
while True:
    current = read_file()
    if initial != current:
        for line in current:
            if line not in initial:
                print(line)
        initial = current