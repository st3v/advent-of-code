from sys import argv

with open(argv[1]) as file:
    times = []
    distances = []
    for line in file:
        key, data = line.strip().split(":")
        key = key.strip()
        data = [int(d.strip()) for d in data.strip().split()]
        if key == "Time":
            times = data
        elif key == "Distance":
            distances = data
    races = zip(times, distances)

total = 1
for time, record in races:
    wins = 0
    for seconds in range(time - 1):
        distance = (time - seconds) * seconds
        if distance > record:
            wins += 1
    total *= wins

print(total)
