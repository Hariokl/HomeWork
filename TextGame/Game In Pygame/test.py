map_name = "map_1"
with open("maps.txt") as maps_file:
    # троичная системма счистления получилась :D
    translate = {"0": "00", "1": "01", "2": "02", "3": "10", "4": "11"}
    readlines = False
    map_tiles = list()

    for line in maps_file.readlines():
        line = line.replace("\n", "")
        if line[2:] != map_name and not readlines:
            continue
        readlines = True

        if line[2:] == map_name:
            continue

        if line == "" and readlines:
            break

        map_tiles.append([translate[x] for x in line])