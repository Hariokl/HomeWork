from random import choice
from time import sleep

status = "choose_room"
room_n = 0
boss_room = 10
m_name = 'монстр'

rooms_choices = {"Комната с монстром": 1, "Неизвестная комната": 2}
player_n = {"max_hp": 20, 'hp': 20, 'dmg': 5, "heal": 2}
monster_prototype_n = {"max_hp": 5, 'hp': 5, 'dmg': 2, 'heal': 2}
player = {"max_hp": 20, 'hp': 20, 'dmg': 5, "heal": 2}
monster_prototype = {"max_hp": 5, 'hp': 5, 'dmg': 2, 'heal': 2}
monster = monster_prototype.copy()
monster_killed = False

while True:
    if status == 'choose_room':
        room_n += 1
        if room_n == boss_room:
            print('\x1b[33mПеред вами дверь босса.\x1b[0m')
            sleep(1)
            print('\x1b[36mЗаходи, как только собирёшься с мыслями.\x1b[0m')
            sleep(1)
            print(f"\x1b[36m\t1.Комната босса\x1b[0m")
            p_choice = input()
            while p_choice != '1':
                p_choice = input()
            print('\x1b[33mВы зашли в комнату босса.\x1b[0m')
            status = 'in_monster_room'
            m_name = 'босс'
            continue
        print("\x1b[33mПеред вами 3 двери.\x1b[0m")
        sleep(0.5)
        print("\x1b[36mВыбери куда хотите пойти.\x1b[0m")
        sleep(0.5)
        rooms = list()
        for i in range(3):
            if choice([1]*9+[0]) == 0:
                rooms.append("Неизвестная комната")
            else:
                rooms.append("Комната с монстром")
        print(f"\x1b[36m\t1.{rooms[0]}\n\t2.{rooms[1]}\n\t3.{rooms[2]}\x1b[0m")
        p_choice = int(input())
        while p_choice not in [1, 2, 3]:
            p_choice = int(input())
        print("<"+"-"*30+">")
        print(f"\x1b[33m\tВы вошли в комнату {room_n}\x1b[0m")
        if rooms_choices[rooms[p_choice - 1]] == 1:
            status = 'in_monster_room'
        elif rooms_choices[rooms[p_choice - 1]] == 2:
            status = 'in_unknown_room'
        print("<"+"-"*30+">")
        sleep(2)
    if status == 'in_unknown_room':
        print('\x1b[33mВы вошли в неизвестную комнату.\x1b[0m')
        sleep(1)
        print('\x1b[33mПеред вами стоит книжка застраховки\x1b[0m')
        sleep(0.5)
        print('\x1b[36mЗастраховать ваше тело?\x1b[0m')
        p_choice = input()
        while p_choice.lower() not in ['да', 'нет']:
            p_choice = input()
        if p_choice.lower() == 'да':
            print('\x1b[33mВаше тело ощущает силу из-за роста уверенности в своём благополучии!\x1b[0m')
            sleep(1)
            print('\x1b[36mВы получили +5 к хп; +2 к силе; +1 к лечению\x1b[0m')
            player['max_hp'], player['hp'] = player['max_hp'] + 5, player['max_hp'] + 5
            player['dmg'], player['heal'] = player['dmg'] + 2, player['heal'] + 1
            status = 'choose_room'
            sleep(1.5)
        else:
            print('\x1b[33mВы отказались застраховывать ваше тело в какой-то книжке\x1b[0m')
        print("<"+"-"*30+">")
    if status == 'in_monster_room':
        sleep(1)
        print(f"\x1b[33mПеред вами {m_name}!\x1b[0m")
        sleep(1)
        print("\x1b[33mОн нападает на вас!\x1b[0m")
        status = 'in_monster_fight'
        mp = monster_prototype
        if m_name == 'босс':
            mp["max_hp"] = 7 * room_n
            mp["hp"] = mp["max_hp"]
            mp["dmg"] = 1 * room_n + 3
            mp['heal'] += 3
        else:
            mp["max_hp"] = 5 * room_n
            mp["hp"] = mp["max_hp"]
            mp["dmg"] = 1 * room_n + 1
        monster = mp.copy()
        sleep(2)
    if status == 'in_monster_fight':
        print("\x1b[33mВы ходите.\x1b[0m")
        sleep(1)

        l1, l11 = len("Игрок|"), len(m_name)
        l2, l12 = len(f"Хп: {player['hp']}/{player['max_hp']}|"), len(f"Хп: {monster['hp']}/{monster['max_hp']}")
        l3, l13 = len("Урон: 5|"), len("Урон: 2")
        l4, l14 = len("Лечение: 3|"), len("Лечение: 2")
        p_hp = f"||Хп: {player['hp']}/{player['max_hp']}{' ' * (l4 - l2)}||"
        m_hp = f"||Хп: {monster['hp']}/{monster['max_hp']}{' ' * (l14 - l12)}||"
        p_dmg = f"||Сила: {player['dmg']}{' ' * (l4 - l3)}||"
        m_dmg = f"||Сила: {monster['dmg']}{' ' * (l14 - l13)}||"

        print("\x1b[33m", '=' * (len('||Лечение: 3||\t||Лечение: 2||') + 1), "\x1b[0m", sep='')
        print(f"\x1b[36m||Игрок{' ' * (l4 - l1)}||\x1b[0m\t\x1b[31m||{m_name.capitalize()}{' ' * (l14 - l11)}||\x1b[0m")
        print(f"\x1b[36m{p_hp}\x1b[0m\t\x1b[31m{m_hp}\x1b[0m")
        print(f"\x1b[36m{p_dmg}\x1b[0m\t\x1b[31m{m_dmg}\x1b[0m")
        print(f"\x1b[36m||Лечение: {player['heal']}||\x1b[0m\t\x1b[31m||Лечение: {monster['heal']}||\x1b[0m")
        print("\x1b[33m", '=' * (len('||Лечение: 3||\t||Лечение: 2||') + 1), "\x1b[0m", sep='')

        print("\x1b[36mВыбирите одно из действий:\x1b[0m")
        print(f"\x1b[36m\t1.Атаковать {m_name}а(x1)\n\t2.Лечить себя(+{player['heal']}хп)\x1b[0m")
        p_choice = int(input())
        while p_choice not in [1, 2]:
            p_choice = int(input())
        if p_choice == 1:
            monster['hp'] -= player['dmg']
            sleep(0.5)
            print(f'\x1b[33mВы атаковали {m_name}а\x1b[0m')
            if monster["hp"] <= 0:
                sleep(1)
                print("<"+"-"*30+">")
                print(f"\x1b[33mВы убили {m_name}а!\x1b[0m")
                print("<"+"-"*30+">")
                sleep(1)
                if m_name == 'босс':
                    sleep(1)
                    print("<" + "-" * 30 + ">")
                    print('\x1b[33mПоздравляем вас, о великий герой, вы победили зло!\x1b[0m')
                    print("<" + "-" * 30 + ">")
                    sleep(1)
                    print('\x1b[36mХотите ли вы переиграть?\x1b[0m')
                    p_choice = input()
                    if p_choice in ['да', 'конечно', 'давай']:
                        monster_prototype = monster_prototype_n
                        monster = monster_prototype_n
                        player = player_n
                        status = 'choose_room'
                        m_name = 'монстр'
                        room_n = 0
                        print("<" + "-" * 60 + ">")
                        print("<" + "-" * 60 + ">")
                        print("<" + "-" * 60 + ">")
                        continue
                status = 'choose_room'
                monster_killed = True
                sleep(1)
                print('\x1b[33mВы ощущаете приток сил после великолепной победы!\x1b[0m')
                sleep(1)
                print('\x1b[33mВы получили +3 к хп; +1 к силе\x1b[0m')
                player['max_hp'], player['hp'] = player['max_hp'] + 3, player['hp'] + 3
                player['dmg'] = player['dmg'] + 1
                sleep(1.5)
        elif p_choice == 2:
            if player['hp'] + player['heal'] <= player["max_hp"]:
                player['hp'] = player['hp'] + player['heal']
            else:
                player["hp"] = player["max_hp"]
            print("\x1b[33mВы вылечили себя\x1b[0m")
        if not monster_killed:
            if (monster["hp"] - player['dmg'] <= 0) and \
                    (min(monster["hp"] + monster["heal"], monster['max_hp']) - player['dmg'] > 0) \
                    and choice([1]*17+[0]*3) == 1:
                sleep(1)
                print(f"\x1b[31mМонстр решил вылечить себя на {monster['heal']}хп.\x1b[0m")
                sleep(2)
                monster['hp'] += monster['heal']
                if monster['hp'] > monster['max_hp']:
                    monster['hp'] = monster['max_hp']
                print("<" + "-" * 30 + ">")
            else:
                print(f"\x1b[31mМонстр решил атаковать вас!\x1b[0m")
                sleep(1)
                print(f"\x1b[31mВы потеряли {monster['dmg']}хп.\x1b[0m")
                sleep(2)
                print("<" + "-" * 30 + ">")
                player['hp'] -= monster['dmg']
            sleep(1)
            if player['hp'] <= 0:
                print("<" + "-" * 30 + ">")
                print('\x1b[31mВы проиграли!\x1b[0m')
                print("<" + "-" * 30 + ">")
                sleep(2)
                print('\x1b[33mХотите попробовать снова?\x1b[0m')
                p_choice = input()
                if p_choice.lower() in ['да', 'давай', 'конечно']:
                    monster_prototype = monster_prototype_n
                    monster = monster_prototype_n
                    player = player_n
                    m_name = 'монстр'
                    status = 'choose_room'
                    room_n = 0
                    print("<" + "-" * 60 + ">")
                    print("<" + "-" * 60 + ">")
                    print("<" + "-" * 60 + ">")
                else:
                    print("<" + "-" * 30 + ">")
                    print('\x1b[33mИгра закончена\x1b[0m')
                    print("<" + "-" * 30 + ">")
                    break
        else:
            monster_killed = False
