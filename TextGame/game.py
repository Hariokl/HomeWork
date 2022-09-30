class Player:
    base = {'hp': 10, 'cards': ['11003'], 'mcg': 3, 'all_cards': ['11003']}
    # mcg - max cards in game
    # В cards первая цифра - на кого действует(1 - на врага, 2 - на себя).
    # Вторая цифра - если первая 1, то урон если 1 и дебафф если 0; если первая 0, то лечение если 1,
    # и бафф если 0.
    # Третья есть ли перезарядка(цифра-перезарядка навыка) или нет(0)
    # Четвёртая цифра - какой именно бафф(Усиление, Доп ход) / дебафф(0 - если это не дебаф или баф)
    # Пятая цифра - на сколько урон/лечение/бафф/дебафф

    def __init__(self):
        self.hp = Player.base['hp']
        self.cards = Player.base['cards']
        self.mcg = Player.base['mcg']
        self.all_cards = Player.base['all_cards']


class Monster:
    base = {'hp': 5, 'cards': ['11002'], 'mcg': 3}

    def __init__(self):
        self.hp = Monster.base['hp'] * 1.2**room_n
        self.cards = Monster.base['cards']
        self.mcg = Monster.base['mcg']


def make_choice(spisok):
    for i, x in enumerate(spisok):
        print(f"{i+1}.{x}")
    print()
    return input('>>').lower()

player = Player()
monster = None
room_status = 'бой'
game_status = 'in_menu'
turn = 1, 0
room_n = 1
while True:
    print('\n' * 10)
    if game_status == 'in_menu':
        print('Меню')
        choice = make_choice(['Играть', 'Правила', 'Настройки'])
        print('\n'*3)
        if choice in ['1', '2', '3', 'и', 'п', 'н']:
            if choice in ['1', 'и']:
                game_status = 'game'
            elif choice in ['2', 'п']:
                game_status = 'rules'
            elif choice in ['3', 'н']:
                game_status = 'settings'
        continue
    if game_status == 'rules':
        print('Правила')
        print('Игрок может сходить от 2 до 3 раз за ход.')
        print('В игре есть Артефакты и Карты.')
        print('Карты')
        print('Карты - это активные умения.')
        print('Карты ты используешь для атаки/лечения/баффа/дебаффа себя или врага.')
        print('Карты можно получить с монстров')
        print('Артефакты')
        print('Артефакты - это пассивные умения.')
        print('Артефакты используются/активны всегда. Вне битвы и в битве.')
        print('Артефакты можно получить получая с монстров.')

        choice = make_choice(['Назад'])
        if choice == '1':
            game_status = 'in_menu'
        continue
    if game_status == 'settings':
        print('Настройки')
        choice = make_choice(['Уровень сложности', 'Выход из игры', 'Назад'])
        if choice in ['1', '2', '3', 'у', 'в', 'н']:
            if choice in ['1', 'у']:
                game_status = 'change_difficulty'
            elif choice in ['2', 'в']:
                exit()
            elif choice in ['3', 'н']:
                game_status = 'in_menu'
        continue
    if game_status == 'change_difficulty':
        print('Смена сложности')
        choice = make_choice(['Обычная', 'Сложная', 'Ад', 'Назад'])
        if choice in ['1', '2', '3', '4', 'о', 'с', 'а', 'н']:
            if choice in ['1', 'о']:
                game_difficulty = 1
            elif choice in ['2', 'с']:
                game_difficulty = 2
            elif choice in ['3', 'а']:
                game_difficulty = 3
            elif choice in ['4', 'н']:
                game_status = 'in_menu'
        continue

    if room_status == 'бой':
        if turn[0] == 1:
            monster = Monster()
        if turn[1] == 0:
            player.turn()
        if turn[1] == 1:
            monster.turn()
