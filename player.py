class Player:
    player_count = 0
    used_names = []

    def __init__(self, name):
        """
        Initializes a new player.

        Args:
            name (str): The name of the player.

        Raises:
            Exception: If the player count exceeds the maximum allowed (8) or if the name is already in use.
        """
        if Player.player_count < 8:
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
        """
        Adds money to the player's balance.

        Args:
            amount (int): The amount of money to add.
        """
        self.money += amount

    def spend_money(self, amount):
        """
        Subtracts money from the player's balance and removes the player if the balance becomes negative.

        Args:
            amount (int): The amount of money to subtract.
        """
        self.money -= amount
        if self.money < 0:
            self.remove_player()

    def los(self):
        """
        Adds $2,000,000 to the player's balance as part of the 'Go' action.
        """
        self.add_money(2000000)

    def get_money(self):
        """
        Gets the current balance of the player.

        Returns:
            int: The player's current balance.
        """
        return self.money

    def remove_player(self):
        """
        Removes the player from the game if their balance becomes negative.
        """
        print(f"Player {self.name} is out of the game.")
        self.is_active = False
        Player.player_count -= 1
