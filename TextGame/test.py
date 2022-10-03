def make_choice(self):
    for i, x in enumerate(self.cards):
        if i not in [y[0] for y in self.cards_in_reload]:
            understand_and_play(self, player)
            r = translate_to_fight(x)
            print('Монстр'+r[0]+'.', r[1])
            sleep(1)


def check_hp(self):
    if self.hp <= 0:
        if self == monster:
            print('Монстр пал.')
            monster = None
        if self == player:
            print('Игрок пал.')
            player = None
    
    
def translate_to_fight(card):
    if card[:3] == '110':
        return 'атакует вас', f'Вы потеряли {card[4:]}хп'
    if card[:3] == '011':
        return 'лечится', f'Монстр вылеил {card[4:]}хп'
