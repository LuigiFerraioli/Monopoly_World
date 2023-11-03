import tkinter as tk
from tkinter import ttk
from player import Player
import random
import locale

class PlayerSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Setup")

        self.players = []
        
        self.label = tk.Label(root, text="Enter player names (2-6 players):", font=("Helvetica", 20))
        self.label.pack()

        self.player_entries = []

        locale.setlocale(locale.LC_ALL, '') 
        for i in range(6):
            label = tk.Label(root, text=f"Player {i + 1}:", font=("Helvetica", 16))
            label.pack()
            entry = tk.Entry(root, font=("Helvetica", 16))
            entry.pack()
            self.player_entries.append(entry)

        self.submit_button = tk.Button(root, text="Start Game", font=("Helvetica", 16), command=self.start_game)
        self.submit_button.pack()

    def start_game(self):
        player_names = [entry.get() for entry in self.player_entries if entry.get()]
        if len(player_names) != len(set(player_names)):
            error_message = tk.Label(self.root, text="Player names must be unique.", font=("Helvetica", 16), fg="red")
            error_message.pack()
        else:
            num_players = len(player_names)
            if 2 <= num_players <= 6:
                self.create_player_windows(player_names)
            else:
                error_message = tk.Label(self.root, text="Please enter 2 to 6 player names.", font=("Helvetica", 16), fg="red")
                error_message.pack()

    def create_player_windows(self, player_names):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        num_players = len(player_names)
        
        if num_players <= 3:
            # Bei bis zu 3 Spielern alle Dimensionen optimal nutzen
            player_width = screen_width // num_players
            player_height = screen_height
        else:
            # Bei mehr als 3 Spielern 3 Spieler oben, der Rest unten
            player_width = screen_width // 3
            player_height = screen_height // 2


        for i, name in enumerate(player_names):
            player = Player(name)
            self.players.append(player)
            player_window = tk.Toplevel(self.root)
            player_window.title(name)
            color = self.random_color()
            label = tk.Label(player_window, text=f"{name}", font=("Helvetica", 24, "bold"), bg=color)
            label.pack()

            money_value = locale.format_string ("%d", player.get_money(), grouping=True)
            money_label = tk.Label(player_window, text=f"Money: {money_value}$", font=("Helvetica", 22, "bold"), bg=color)
            money_label.pack()

            empty_label = tk.Label(player_window, bg=color)
            empty_label.pack()

            add_money_entry = tk.Entry(player_window, font=("Helvetica", 16))
            add_money_entry.pack()
            add_money_button = tk.Button(player_window, text="Add Money", font=("Helvetica", 16),
                                        command=lambda player=player, entry=add_money_entry, money_label=money_label: self.add_money(player, entry, money_label))
            add_money_button.pack()

            empty_label = tk.Label(player_window, bg=color)
            empty_label.pack()

            spend_money_entry = tk.Entry(player_window, font=("Helvetica", 16))
            spend_money_entry.pack()
            spend_money_button = tk.Button(player_window, text="Spend Money", font=("Helvetica", 16),
                                        command=lambda player=player, entry=spend_money_entry, money_label=money_label: self.spend_money(player, entry, money_label))
            spend_money_button.pack()

            empty_label = tk.Label(player_window, bg=color)
            empty_label.pack()

            miete_label = tk.Label(player_window, text="Rent to and $$:", font=("Helvetica", 16))
            miete_label.pack()

            other_player_names = [p_name for p_name in player_names if p_name != name]

            miete_var = tk.StringVar(player_window)
            miete_var.set(other_player_names[0] if other_player_names else "")

            miete_menu = ttk.Combobox(player_window, textvariable=miete_var, values=other_player_names)
            miete_menu.pack()

            miete_amount_entry = tk.Entry(player_window, font=("Helvetica", 16))
            miete_amount_entry.pack()

            miete_button = tk.Button(player_window, text="Pay Rent", font=("Helvetica", 16),
                                command=lambda p=player, m=miete_menu, amount=miete_amount_entry, money_label=money_label: self.pay_rent(p, m, amount, money_label))
            miete_button.pack()

            empty_label = tk.Label(player_window, bg=color)
            empty_label.pack()

            los_button = tk.Button(player_window, text="START", font=("Helvetica", 16),
                                command=lambda p=player, money_label=money_label: self.run_los(p, money_label))
            los_button.pack()

            empty_label = tk.Label(player_window, bg=color)
            empty_label.pack()

            player.money_label = money_label  # Das Geld-Label des Spielers speichern

            player.status_label = tk.Label(player_window, text="Active", font=("Helvetica", 16), fg="green")
            player.status_label.pack()

            player_window.protocol("WM_DELETE_WINDOW", lambda p=player, w=player_window: self.on_player_window_close(p, w))
            player_window.configure(bg=color)

            # Position der Spieler-GUI basierend auf der Anzahl der Spieler und den Bildschirmabmessungen
            player_window.geometry(f"{player_width}x{player_height}+{i * player_width}+0" if i < 4 else f"{player_width}x{player_height}+{(i - 4) * player_width}+{player_height}")

    def on_player_window_close(self, player, window):
        Player.player_count -= 1
        Player.used_names.remove(player.name)
        self.players.remove(player)
        window.destroy()


    def add_money(self, player, entry, money_label):
        if player.is_active:
            try:
                amount = int(entry.get())
                player.add_money(amount)
                
                # Formatieren und anzeigen des Geldbetrags mit Tausendertrennzeichen
                money_value = locale.format_string ("%d", player.get_money(), grouping=True)
                money_label.config(text=f"Money: {money_value}$")
            except ValueError:
                pass
            entry.delete(0, tk.END)

    def spend_money(self, player, entry, money_label):
        if player.is_active:
            try:
                amount = int(entry.get())
                player.spend_money(amount)
                money_value = locale.format_string ("%d", player.get_money(), grouping=True)
                money_label.config(text=f"Money: {money_value}$")
                if player.get_money() < 0:
                    player.status_label.config(text="Out of Game", fg="red")
                    player.is_active = False
                    if self.get_active_players_count() == 1:
                        winner = self.get_active_players()[0]
                        winner.status_label.config(text="Winner!", fg="green")
            except ValueError:
                pass
            entry.delete(0, tk.END)

    def run_los(self, player, money_label):
        if player.is_active:
            try:
                player.los()
                money_value = locale.format_string ("%d", player.get_money(), grouping=True)
                money_label.config(text=f"Money: {money_value}$")
            except ValueError:
                pass

    def pay_rent(self, payer, miete_menu, amount_entry, money_label):
        if payer.is_active:
            try:
                recipient_name = miete_menu.get()
                amount = amount_entry.get()
                if amount.isdigit():
                    amount = int(amount)
                    for recipient in self.players:
                        if recipient.name == recipient_name:
                            if payer.get_money() >= amount:
                                payer.spend_money(amount)
                                recipient.add_money(amount)
                                money_value = locale.format_string ("%d", payer.get_money(), grouping=True)
                                money_label.config(text=f"Money: {money_value}$")
                                amount_entry.delete(0, tk.END)
                                
                                # Aktualisiere auch das GUI des Empfängers
                                recipient_money_value = locale.format_string ("%d", recipient.get_money(), grouping=True)
                                recipient.money_label.config(text=f"Money: {recipient_money_value}")
                                
                                return
                            else:
                                # Überweise verbleibendes Geld an den Empfänger und ändere den Status des Payers
                                recipient.add_money(payer.get_money())
                                payer.spend_money(payer.get_money())
                                money_value = locale.format_string ("%d", payer.get_money(), grouping=True)
                                money_label.config(text=f"Money: {money_value}$")
                                amount_entry.delete(0, tk.END)
                                money_value = locale.format_string ("%d", payer.get_money(), grouping=True)
                                money_label.config(text=f"Money: {money_value}$")
                                payer.status_label.config(text="Out of Game", fg="red")
                                payer.is_active = False
                                # Aktualisiere auch das GUI des Empfängers
                                recipient_money_value = locale.format_string ("%d", recipient.get_money(), grouping=True)
                                recipient.money_label.config(text=f"Money: {recipient_money_value}")
                                
                                payer.remove_player()
                                money_label.config(fg="red")  # Ändere die Farbe des Geldbetrags, um den Verlust anzuzeigen
                                return
            except ValueError:
                pass

        # Fehlernachricht anzeigen, wenn der Empfänger, Betrag oder das Geld des Payers ungültig ist
        error_message = tk.Label(self.root, text="Invalid recipient, amount, or insufficient funds", font=("Helvetica", 16), fg="red")
        error_message.pack()

    def get_active_players(self):
        return [player for player in self.players if player.is_active]

    def get_active_players_count(self):
        return len(self.get_active_players())

    def random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerSetupGUI(root)
    root.mainloop()
