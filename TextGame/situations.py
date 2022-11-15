
from random import randint


class Way:
    ways = dict()
    ways_class_dict = dict()
    ways_class_parent = dict()

    def __init__(self, n, *ways):
        self.ways = ways
        self.n = n
        Way.ways[n] = [way.n for way in ways]
        Way.ways_class_dict[n] = self


def create_ways(n, ns="1"):
    if n == 1:
        return Way(ns)
    return Way(ns, *[create_ways(n-1, ns+str(i+1)) for i in range(2)])


rooms = 10
room_n = 0
time = 60
cur_pos = "1"
cur_way = None
playing = True

while playing:
    print("\n"*10)
    if room_n == -1:
        print("Выберите сложность игры:")
        choices = [f"\t{i+1}. {x}" for i, x in enumerate(("Для АБ", "Для лохов", "Лёгкая", "Назад"))]
        player_chose = input("\n\n\n>>>")
        while player_chose.lower() not in [str(i+1) for i in range(len(choices) + (1 if len(cur_pos) > 1 else 0))]+["аб", "лох", "лохов"] and \
                player_chose.lower() not in [x.split()[-1].lower() for x in choices]:
            player_chose = input(">>>")
        if player_chose.lower() in ["для аб", "1", "аб"]:
            rooms = 3
        elif player_chose.lower() in ["для лохов", "лохов", "1", "лох"]:
            rooms = 5
        elif player_chose.lower() in ["4", "назад"]:
            room_n = 0
        else:
            rooms = 10
    
    if room_n == 0:
        choices = [f"\t{i+1}. {x}" for i, x in enumerate(("Начать игру", "История", "Сложность", "Выйти"))]
        print("\n".join(choices))
        player_chose = input("\n\n\n>>>")
        while player_chose.lower() not in [str(i+1) for i in range(len(choices) + (1 if len(cur_pos) > 1 else 0))] and \
                player_chose.lower() not in [x.split()[-1].lower() for x in choices]:
            player_chose = input(">>>")
        if player_chose.lower() in ["1", "начать", "начать игру"]:
            room_n = 1
            create_ways(rooms)
            destination = "1" + "".join(str(randint(1, 2)) for _ in range(rooms-1))
        elif player_chose.lower() in ["2", "история"]:
            print("\n"*10)
            print("Вы съели у АБ его шаурму и об этом он узнаёт. Разгневанный АБ бежит за вами, и вы с ним попадаете в лабиринт. Дойдите до конца, чтобы получить шаурму на выходе лабиринта. Но помните: у вас не так много времени-60 секунд-за это время АБ успеет добежать до вас.")
            input("\n\n\n>>>")
            continue
        elif player_chose.lower() in ["3", "сложность"]:
            room_n = -1
        else:
            exit()
        continue
        
    print(f"Комната: {room_n}")
    print("Выберите путь:")
    choices = [f"\t{i+1}. {x}" for i, x in enumerate(("Налево", "Направо")) if cur_pos+str(i+1) in Way.ways_class_dict]
    if len(choices) != 0:
        print("\n".join(choices))
    if len(cur_pos) > 1:
        print(f"\t{len(choices) + 1}. Вернуться")
    print("\n"*4)

    player_chose = input(">>>")
    while player_chose.lower() not in [str(i+1) for i in range(len(choices) + (1 if len(cur_pos) > 1 else 0))] and \
            player_chose.lower() not in [x.split()[-1].lower() for x in choices] + \
            (["вернуться"] if len(cur_pos) > 1 else []):
        player_chose = input(">>>")
    if player_chose.lower() in ["1", "налево", "лево"] and len(choices) == 2:
        cur_pos += "1"
    elif player_chose.lower() in ["2", "направо", "право"] and len(choices) == 2:
        cur_pos += "2"
    else:
        cur_pos = cur_pos[:-1]
        room_n -= 2
    room_n += 1
    cur_way = Way.ways_class_dict[cur_pos]

    if len(cur_pos) == rooms:
        if cur_pos == destination:
            print("Поздравляю! Вы сбежали от сгневаного АБ.")
            print("Конец.")
            playing = False
        else:
            print("Перед вами тупик. Может, попробуете вернуться?")
