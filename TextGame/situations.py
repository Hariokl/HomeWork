from time import perf_counter
from random import randint


class Player:
    def __init__(self):
        self.cur_pos = "1"
        self.cur_way = None
        self.room_n = 0
        self.bag = {"Шаурма": 0}

    def get_item(self, item):
        self.bag[item] += 1


class Way:
    destination = None
    left = ["1 + 1 - 2 + 1", "2 - 1", "sin(90*)", "sin(-270*)", "10 / 2 * 10 // 25 - 1",
            "У Васи три яблока в правой руке и два в левой.\nУ него отняли два яблока из правой руки. " "В какой руке больше яблок?",
            "6! / 720", "30 + 1 / 1 - 1 - 31 + 2"]
    right = ["(1 + 2 + 3 + 4) / 5", "cos(90*) + 2", "sin(-270*) + sin(90*)", "10 / 2 * 10 // 25",
             "2 + 5 - 3 - 2", "100 // 10 - 5 + 16 - 27 - 4",
             "Левый спортсмен бегает быстрее правого на 13 км/час.\n" "Кто из них придёт позже, если оба начанали одновременно?",
             "Шарик + Банан = 3 Банана\n" "Шарик = 4\nЧему равен Банан?"]
    unknown = [
        "У Васи три яблока в правой руке и два в левой.\n" "У него украли яблоки из сумки. Как зовут отца Пети?",
        "1 + 1 - 2 + 1 - 5", "tg(90*)", "100 // 10 - 5 + 16 - 27 - 10", "cos(90*) + 4"]

    ways = dict()
    ways_class_dict = dict()

    def __init__(self, n, *ways):
        ways_to_d = {True: (Way.left, Way.right), False: (Way.unknown, Way.unknown)}
        self.ways = ways
        self.n = n
        self.way_to_d = None
        self.zad = None
        if len(n) != len(Way.destination):
            self.zad = ways_to_d[n == Way.destination[:len(n)]][int(Way.destination[len(n)]) - 1]
            self.zad = self.zad[randint(0, len(self.zad) - 1)]

        Way.ways[n] = [way.n for way in ways]
        Way.ways_class_dict[n] = self


def create_ways(n, ns="1"):
    if n == 1:
        return Way(ns)
    return Way(ns, *[create_ways(n - 1, ns + str(i + 1)) for i in range(2)])


class Game:
    def __init__(self):
        self.bag = []

    def run(self):
        player = Player()
        rooms = 10
        room_n = 0
        ab_room_n = 0
        ab_room_v = 3, 10
        ab_v = 2
        cur_pos = "1"
        cur_way = None
        playing = True
        while playing:
            print("\n" * 10)
            if player.bag["Шаурма"] > 0 and room_n == ab_room_n:
                print("Перед вами АБ. Что будете делать?")
                print("\n".join([f"\t{i}. {x}" for i, x in
                                 enumerate(["Посмотреть рюкзак", "Дать Священную Шаурму"])]))
                player_chose = input(">>>").lower()
                if player_chose in ["1", "посмотреть", "посмотреть рюкзак"]:
                    print("Рюкзак: " + ''.join([f"{x}x{player.bag[x]}" for x in player.bag]))
                    input()
                    continue
                elif player_chose in ["2", "дать", "дать священную шаурму", "дать священную"]:
                    pass
                else:
                    player.bag["Шаурма"] = 0
                    continue
                print(
                    "Вы отдаёте АБ Шаурму. Но неожиданно для вас,"
                    "\nАБ останавливается перед великолепием шаурмы. Он ещё долго стоит и пускает слюни. "
                    "\nВы решаетесь взять шаурму и протянуть её ему. Он съедает её за секунды и довольный прощает вас. "
                    "\n\tВы выжили!")
                print("Конец.")
                input()
                room_n = 0
                player.bag["Шаурма"] = 0
                continue
            elif player.bag["Шаурма"] == 0 and room_n == ab_room_n != 0:
                print("Вас поймал АБ и приготовил из вас шаурму.")
                print("Конец.")
                input()
                room_n = 0
                player.bag["Шаурма"] = 0
                continue
            if room_n == -1:
                print("Выберите сложность игры:")
                choices = [f"\t{i + 1}. {x}" for i, x in
                           enumerate(("Для АБ", "Для лохов", "Лёгкая", "Назад"))]
                print("\n".join(choices))
                player_chose = input("\n>>>")
                while player_chose.lower() not in [str(i + 1) for i in
                                                   range(len(choices) + (
                                                   1 if len(cur_pos) > 1 else 0))] + [
                    "аб", "лох", "лохов"] and \
                        player_chose.lower() not in [x.split()[-1].lower() for x in choices]:
                    player_chose = input(">>>")
                if player_chose.lower() in ["для аб", "1", "аб"]:
                    rooms = 3
                elif player_chose.lower() in ["для лохов", "лохов", "1", "лох"]:
                    rooms = 5
                elif player_chose.lower() in ["4", "назад"]:
                    room_n = 0
                else:
                    rooms = 10
                continue

            if room_n == 0:
                choices = [f"\t{i + 1}. {x}" for i, x in
                           enumerate(("Начать игру", "История", "Сложность", "Выйти"))]
                print("\n".join(choices))
                player_chose = input("\n>>>")
                while player_chose.lower() not in [str(i + 1) for i in
                                                   range(len(choices) + (
                                                   1 if len(cur_pos) > 1 else 0))] and \
                        player_chose.lower() not in [x.split()[-1].lower() for x in choices]:
                    player_chose = input(">>>")
                if player_chose.lower() in ["1", "начать", "начать игру"]:
                    room_n = 1
                    Way.destination = "1" + "".join(str(randint(1, 2)) for _ in range(rooms - 1))
                    create_ways(rooms)
                    cur_pos = "1"
                    cur_way = Way.ways_class_dict[cur_pos]
                    ab_room_n = 0
                elif player_chose.lower() in ["2", "история"]:
                    print("\n" * 10)
                    print("""Вы съели у АБ его шаурму и об этом он узнаёт. 
        Разгневанный АБ бежит за вами, и вы с ним попадаете в лабиринт. 
        Дойдите до конца, чтобы получить шаурму на выходе лабиринта. 
        Но помните: у вас не так много времени-60 секунд-за это время АБ успеет добежать до вас.""")
                    input("\n>>>")
                    continue
                elif player_chose.lower() in ["3", "сложность"]:
                    room_n = -1
                else:
                    exit()
                continue

            print(f"Комната: {room_n}")
            print(f"Время на выбор: {ab_room_v[1]}")
            zad = cur_way.zad
            zad = "Вы где-то лоханулись" if zad is None else zad
            print(f"Задача: {zad}")
            print("Выберите путь:")
            choices = [f"\t{i + 1}. {x}" for i, x in enumerate(("Налево", "Направо")) if
                       cur_pos + str(i + 1) in Way.ways_class_dict]
            if len(choices) != 0:
                print("\n".join(choices))
            if len(cur_pos) > 1:
                print(f"\t{len(choices) + 1}. Вернуться")
            start = perf_counter()
            player_chose = input("\n>>>")
            while player_chose.lower() not in [str(i + 1) for i in
                                               range(len(choices) + (
                                               1 if len(cur_pos) > 1 else 0))] and \
                    player_chose.lower() not in [x.split()[-1].lower() for x in choices] + \
                    (["вернуться"] if len(cur_pos) > 1 else []):
                player_chose = input(">>>")
            end = perf_counter()
            print(end - start, room_n - ab_room_n)
            if end - start >= ab_room_v[1] or room_n - ab_room_n >= ab_room_v[0]:
                ab_room_n += 1
            if ab_room_n == room_n and player.bag["Шаурма"] == 0:
                print("Вас поймал АБ и приготовил из вас шаурму.")
                print("Конец.")
                input()
                room_n = 0
                continue
            if player_chose.lower() in ["1", "налево", "лево"] and len(choices) == 2:
                cur_pos += "1"
            elif player_chose.lower() in ["2", "направо", "право"] and len(choices) == 2:
                cur_pos += "2"
            else:
                cur_pos = cur_pos[:-1]
                room_n -= 2
            room_n += 1
            cur_way = Way.ways_class_dict[cur_pos]

            if len(cur_pos) == rooms:
                if cur_pos == Way.destination:
                    print("Перед вами что-то летает. Взять?")
                    print("\n".join([f"\t{i}. {x}" for i, x in enumerate(["Взять", "Вернуться"])]))
                    player_chose = input(">>>").lower()
                    if player_chose in ["1", "взять"]:
                        player.get_item("Шаурма")
                    else:
                        room_n -= 1
                        cur_pos = cur_pos[:-1]
                        cur_way = Way.ways_class_dict[cur_pos]
                ###########################################################
                elif cur_pos != Way.destination:
                    print("Перед вами тупик. Может, попробуете вернуться?")


if __name__ == "__main__":
    game = Game()
    game.run()
