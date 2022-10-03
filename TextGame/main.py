from time import sleep


class Player:
    base = {'hp': 10, 'mana': 5, 'cards': ['11003', '11010', '00223'], 'mcg': 3, 'all_cards': ['11003', '11010']}
    # mcg - max cards in game
    # В cards первая цифра - на кого действует(1 - на врага, 0 - на себя).
    # Вторая цифра - если первая 1, то урон если 1 и дебафф если 0; если первая 0, то лечение если 1,
    # и бафф если 0.
    # Третья цифра - какой именно бафф(Усиление, Доп ход) / дебафф(0 - если это не дебаф или баф)
    # Четвёртая есть ли перезарядка(цифра-перезарядка навыка) или нет(0)
    # Пятая цифра - на сколько урон/лечение/бафф/дебафф

    def __init__(self):
        self.hp = Player.base['hp']
        self.lvl = 1
        self.max_hp = Player.base['hp']
        self.mana = Player.base['mana']
        self.cards = Player.base['cards']
        self.mcg = Player.base['mcg']
        self.all_cards = Player.base['all_cards']
        self.cards_in_reload = []
        self.status = []

    def turn(self):
        print('Ваша очередь')
        print(self.hp)

        check_hp(self)

        k = update_status(self)
        if k == 0:
            return

        check_hp(self)
        while True:
            if monster.hp <= 0:
                return
            choice = self.make_choice([self.make_beautiful(translate(x), x) for x in self.cards])
            while choice != '0':
                if choice in [str(x + 1) for x in range(len(self.cards))] and choice.isdigit():
                    if (int(choice) - 1) not in [x[0] for x in self.cards_in_reload]:
                        break
                choice = input('>>').lower()
            if choice == '0':
                break
            card = self.cards[int(choice)-1]
            understand_and_play(self, monster, card)

            self.cards_in_reload.append((int(choice) - 1, int(card[3])))
        cards_in_reload = []
        for i, x in enumerate(self.cards_in_reload):
            x = x[0], x[1] - 1
            if x[1] >= 0:
                cards_in_reload.append(x)
        else:
            self.cards_in_reload = cards_in_reload

    def make_beautiful(self, card, cart):
        bol = None
        stc = 2
        t = 0
        for y in self.cards_in_reload:
            if y[0] == self.cards.index(cart):
                bol = y
                stc = 1
                t = 1
                break
        st = tcolor('='*20, stc)+'\n'
        for x in card.split('/'):
            r = x
            r = tcolor('||', stc) + ' '*((18-len(x))//2) + r + ' '*(
                    (18-len(x))//2+(18-len(x))%2) + tcolor('||', stc) + '\n'
            st += r
        if bol is not None:
            r = f'На перез.:{bol[1]}'
            st += tcolor('||', stc) + ' ' * ((18 - len(r)) // 2) + r + ' ' * (
                        (18 - len(r)) // 2 + (18 - len(r)) % 2) + tcolor('||', stc) + '\n'

        st += (tcolor('||', stc) + ' '*18 + tcolor('||', stc) + '\n') * (3-len(card.split('/'))-t)
        st += tcolor('='*22, stc)

        return st

    def make_choice(self, opt):
        st = ''
        for i in range(5):
            r = ''
            for j, x in enumerate(opt):
                if i == 0:
                    r += f'{j+1}.'
                r += x.split('\n')[i] + ' '*4
            st += r + '\n'
        print(st)
        return input('>>')


class Monster:
    base = {'hp': 5, 'cards': ['11002'], 'mcg': 3}

    def __init__(self):
        self.hp = Monster.base['hp'] * float(f"1.{game_difficulty+2}")**room_n
        self.max_hp = self.hp
        self.cards = Monster.base['cards']
        self.cards_in_reload = []
        self.status = []
        self.mcg = Monster.base['mcg']

    def turn(self):
        global monster
        print(self.hp)
        print('Очередь монстра')

        check_hp(self)
        if monster is None:
            return

        k = update_status(self)
        if k == 0:
            return

        check_hp(self)
        if monster is None:
            return

        self.make_choice()

        cards_in_reload = []
        for i, x in enumerate(self.cards_in_reload):
            x = x[0], x[1] - 1
            if x[1] >= 0:
                cards_in_reload.append(x)
        else:
            self.cards_in_reload = cards_in_reload

    def make_choice(self):
        for i, x in enumerate(self.cards):
            if i not in [y[0] for y in self.cards_in_reload]:
                understand_and_play(self, player, x)
                self.cards_in_reload.append((int(choice) - 1, int(x[3])))
                r = translate_to_fight('Монстр', 'Вы', x, ['', 'и'])
                print(r[0] + '.', r[1])
                sleep(2)


def translate_to_fight(who, whom, card, te=[]):
    st = f'{who} использует{te[0]} карту'
    if card[:3] == '110':
        return f'{st} атаки', f'\n{whom} потерял{te[1]} {card[4:]}хп'
    if card[:3] == '010':
        return f'{st} лечения', f'\n{who} вылечил{te[0]} {card[4:]}хп'
    if card[:3] == '111':
        return f'{st} вампиризма', f"\n{whom} потерял{te[1]} {card[4:]}хп\n{who} вылечил{te[0]} {card[4:]}хп"


def tcolor(ob, ind):
    return f"\x1b[3{ind}m{ob}\x1b[0m"


def update_status(self):
    stop = False
    for i, status in enumerate(self.status):
        if status[0] == '1':
            if status[1] == '1':  # заморозка
                print('Заморожен...')
                print('Пропускает ход...')
                stop = True
            if status[1] == '2':  # горение
                self.hp -= (self.max_hp // 10 + 1)
        if status[0] == '0':
            if status[1] == '1':  # исцеление
                self.hp = min(self.hp + self.max_hp // 5, self.max_hp)
            if status[1] == '2':  # снятие всех эффектов
                self.status = []

    for i, status in enumerate(self.status):
        self.status[i] = status[0] + status[1] + str(int(status[2:]) - 1)
        if int(self.status[i][2:]) <= 0:
            self.status.remove(self.status[i])
    if stop:
        return 0
    return 1


def understand_and_play(self, other, card):
    if card[:3] == '110': # атака
        other.hp -= int(card[4:])
    elif card[:3] == '111': # вампиризм
        other.hp -= int(card[4:])
        self.hp += int(card[4:])
    elif card[:2] == '10': # дебафф
        other.status.append(f'{card[0]}{str(int(card[2])-1)}{card[4:]}')
    elif card[:2] == '00':
        self.status.append(f'{card[0]}{str(int(card[2])-1)}{card[4:]}')
    elif card[:3] == '010': # лечение
        self.hp = min(self.hp + int(card[4:]), self.max_hp)


def translate(card):
    st = ''
    if card[:3] == '110':
        st += f'Атака:{card[4:]}'
    elif card[:3] == '111':
        st += f'Вампиризм:{card[4:]}'
    elif card[:2] == '10':
        st += 'Дебафф'
        if card[2] == '2':
            st += f' заморозка:{card[4:]}'
        if card[2] == '3':
            st += f' горение:{card[4:]}'
    elif card[:2] == '00':
        st += 'Бафф'
        if card[2] == '2':
            st += f' исцеление:{card[4:]}'
        if card[2] == '3':
            st = 'Снятие эффектов'
    elif card[:3] == '010':
        st += f'Лечение:{card[4:]}'
    if card[3] != '0':
        st += f'/Перез.:{card[3]}'
    return st


def check_hp(self):
    global monster, player
    if self.hp <= 0:
        if self == monster:
            print('Монстр пал.')
            monster = None
        if self == player:
            print('Игрок пал.')
            player = None


def make_choice(spisok=[]):
    for i, x in enumerate(spisok):
        print(f"{i+1}.{x}")
    print()
    choice = input('>>').lower()
    while choice not in [str(x+1) for x in range(len(spisok))]:
        choice = input('>>').lower()
    return choice


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
        if monster is None:
            room_status = 'treasure'
            nturn = (1, 0)
            continue
        if nturn[1] == 0:
            player.turn()
            nturn = nturn[0], 1
        if nturn[1] == 1:
            monster.turn()
            nturn = nturn[0] + 1, 0
        continue
    if room_status == 'treasure':
        choice = make_choice(['Card', 'Artefact'])
        continue
