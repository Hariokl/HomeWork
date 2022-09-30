class Player:
    base = {'hp': 10, 'cards': ['11003', '11010'], 'mcg': 3, 'all_cards': ['11003']}
    # mcg - max cards in game
    # В cards первая цифра - на кого действует(1 - на врага, 2 - на себя).
    # Вторая цифра - если первая 1, то урон если 1 и дебафф если 0; если первая 0, то лечение если 1,
    # и бафф если 0.
    # Третья цифра - какой именно бафф(Усиление, Доп ход) / дебафф(0 - если это не дебаф или баф)
    # Четвёртая есть ли перезарядка(цифра-перезарядка навыка) или нет(0)
    # Пятая цифра - на сколько урон/лечение/бафф/дебафф

    def __init__(self):
        self.hp = Player.base['hp']
        self.cards = Player.base['cards']
        self.mcg = Player.base['mcg']
        self.all_cards = Player.base['all_cards']
        self.cards_in_reload = []

    def turn(self):
        print('Ваша очередь')
        choice = make_choice(self.cards)
        if choice in [str(x + 1) for x in range(len(self.cards))]:
            self.understand_and_play(self.cards[int(choice)-1], int(choice) - 1)

    def understand_and_play(self, card, id):
        if card[:3] == '110':
            pass
        elif card[:3] == '001':
            pass
        self.cards_in_reload.append((id, int(card[3])))
        for i, x in enumerate(self.cards_in_reload):
            x = x[0], x[1] - 1
            self.cards_in_reload[i] = x
            if x[1] < 0:
                self.cards_in_reload.remove(x)
        print(self.cards_in_reload)
        monster.hp -= int(card[4:])

    def translate(self, card):
        pass


class Monster:
    base = {'hp': 5, 'cards': ['11002'], 'mcg': 3}

    def __init__(self):
        self.hp = Monster.base['hp'] * float(f"1.{game_difficulty+2}")**room_n
        self.cards = Monster.base['cards']
        self.mcg = Monster.base['mcg']

    def turn(self):
        print('Очередь монстра')
        print(self.hp)
        make_choice()


def make_choice(spisok=[]):
    for i, x in enumerate(spisok):
        print(f"{i+1}.{x}")
    print()
    return input('>>').lower()


player = Player()
monster = None
room_status = 'бой'
game_status = 'in_menu'
game_difficulty = 1
nturn = 1, 0
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
                room_status = 'entered'
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
    if room_status == 'entered':
        print('Вы находитесь в комнате с монстром Слайм')
        choice = make_choice(['Атаковать'])
        if choice in ['1', 'а']:
            if choice in ['1', 'а']:
                room_status = 'fight'
        continue
    if room_status == 'fight':
        if nturn[0] == 1:
            monster = Monster()
        if nturn[1] == 0:
            player.turn()
            nturn = nturn[0], 1
        if nturn[1] == 1:
            monster.turn()
            nturn = nturn[0] + 1, 0
        continue
        
