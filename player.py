class Player:
    player_count = 0
    used_names = []

    def __init__(self, name):
        if Player.player_count < 6:
            if name not in Player.used_names:
                self.name = name
                self.money = 15000000
                self.is_active = True
                Player.used_names.append(name)
                Player.player_count += 1
            else:
                raise Exception(f"Player name '{name}' is already in use.")
        else:
            raise Exception("Maximum of 8 players reached. Cannot create more players.")

    def add_money(self, amount):
        self.money += amount

    def spend_money(self, amount):
        self.money -= amount
        if self.money < 0:
            self.remove_player()

    def los(self):
        self.add_money(2000000)

    def get_money(self):
        return self.money

    def remove_player(self):
        print(f"Player {self.name} is out of the game.")
        self.is_active = False
        Player.player_count -= 1
