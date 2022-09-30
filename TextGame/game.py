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
        self.hp = Monster.base['hp']
        self.cards = Monster.base['cards']
        self.mcg = Monster.base['mcg']


player = Player()
monster = None
room_status = 'бой'
turn = 1, 0
room_n = 1
while True:
    if room_status == 'бой':
        if turn[0] == 1:
            monster = Monster()
        if turn[1] == 0:
            player.turn()
        if turn[1] == 1:
            monster.turn()
