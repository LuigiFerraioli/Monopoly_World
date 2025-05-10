import tkinter as tk
from tkinter import ttk
from player import Player
from PIL import Image, ImageTk
import os
import sys
import random
import locale


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class PlayerSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Monopoly World Bank GUI")
        window_width = 450
        window_height = 500
        self.center_window(window_width, window_height)

        self.max_players = 8
        self.players = []
        self.figure_images = []
        locale.setlocale(locale.LC_ALL, '')

        # Notebook (Tabs)
        style = ttk.Style()
        style.configure("TNotebook", borderwidth=0)
        style.configure("TNotebook.Tab", padding=[10, 5])

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Fehler-Label als grid
        self.error_message = tk.Label(
            self.root, text="", font=("Helvetica", 16), fg="red")

        # Tabs initialisieren
        self.create_player_tab()
        self.create_settings_tab()

    def create_player_tab(self):
        self.setup_frame = tk.Frame(self.notebook)
        self.notebook.add(self.setup_frame, text='Players')

        self.label = tk.Label(
            self.setup_frame, text="Enter player names (2-8 players)", font=("Helvetica", 20))
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.player_entries = []
        for i in range(self.max_players):
            label = tk.Label(self.setup_frame,
                             text=f"Player {i + 1}:", font=("Helvetica", 16))
            label.grid(row=i + 1, column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(self.setup_frame, font=("Helvetica", 16))
            entry.grid(row=i + 1, column=1, padx=10, pady=5, sticky='w')
            self.player_entries.append(entry)

        self.submit_button = tk.Button(self.setup_frame, text="Start Game", font=("Helvetica", 16),
                                       command=self.start_game)
        self.submit_button.grid(row=self.max_players+1,
                                column=0, columnspan=2, pady=10)

    def create_settings_tab(self):
        self.settings_frame = tk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='Settings')

        # Container-Frame zentriert platzieren
        container = tk.Frame(self.settings_frame)
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        title_label = tk.Label(
            container, text="Game Settings", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=15)

        # Startkapital
        start_money_label = tk.Label(container, text="Start Capital:", font=(
            "Helvetica", 14), anchor='e', width=20)
        start_money_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.start_money_var = tk.StringVar(value="15000000")
        start_money_entry = tk.Entry(
            container, textvariable=self.start_money_var, font=("Helvetica", 14), width=12)
        start_money_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # GO Bonus
        go_bonus_label = tk.Label(container, text="Money for passing GO:", font=(
            "Helvetica", 14), anchor='e', width=20)
        go_bonus_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.go_bonus_var = tk.StringVar(value="2000000")
        go_bonus_entry = tk.Entry(
            container, textvariable=self.go_bonus_var, font=("Helvetica", 14), width=12)
        go_bonus_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    def get_numeric_setting(self, var, default=0, error_msg=None):
        try:
            return int(var.get())
        except ValueError:
            if error_msg:
                self.show_error(error_msg)
            return default

    def start_game(self):
        self.start_money = self.get_numeric_setting(
            self.start_money_var, default=15000000)
        self.go_bonus = self.get_numeric_setting(
            self.go_bonus_var, default=2000000)
        self.player_names = [entry.get()
                             for entry in self.player_entries if entry.get()]
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                widget.destroy()  # Alte Fehlermeldungen entfernen
        self.check_game_layout_rules(self.player_names)

    def check_game_layout_rules(self, player_names):
        if len(player_names) != len(set(player_names)):
            self.show_error("Player names must be unique.")
        else:
            num_players = len(player_names)
            if 2 <= num_players <= self.max_players:
                self.clear_window()
                self.create_players_view(player_names)
            else:
                self.show_error("Please enter 2 to 8 player names.")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.root.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_players_view(self, player_names):
        # Neues Frame für das Spielbrett mit Grid
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.game_frame = tk.Frame(self.root)
        self.game_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Root-Fenster auf Grid konfigurieren
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        num_players = len(player_names)
        if num_players == 4:
            num_cols = 2
            num_rows = 2
        elif num_players >= 7:
            num_cols = 4
            num_rows = 2
        else:
            num_cols = min(3, num_players)
            num_rows = (num_players + num_cols - 1) // num_cols

        # Holen und sortiere die Bilddateien für Spielfiguren
        figure_dir = "images/figures"
        figure_files = sorted([f for f in os.listdir(
            figure_dir) if f.endswith((".png", ".gif", ".jpg"))])[:num_players]

        # Konfiguriere Spalten und Zeilen im game_frame für automatisches Resizing
        for row in range(num_rows):
            self.game_frame.rowconfigure(row, weight=1)
        for col in range(num_cols):
            self.game_frame.columnconfigure(col, weight=1)
        for i, (name, figure_file) in enumerate(zip(self.player_names, figure_files)):
            player = Player(name, self.start_money, self.go_bonus)
            self.players.append(player)
            color = self.random_color()

            player_frame = tk.Frame(
                self.game_frame, bd=2, relief="groove", bg=color, padx=10, pady=10)
            player_frame.grid(row=i // num_cols, column=i % num_cols,
                              padx=10, pady=10, sticky="nsew")

            # Lade Bild und speichere Referenz
            img_path = resource_path(os.path.join(
                "images", "figures", figure_file))
            try:
                image = Image.open(img_path).resize(
                    (80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                photo = None
            photo = ImageTk.PhotoImage(image)
            self.figure_images.append(photo)

            top_row = tk.Frame(player_frame, bg=color)
            top_row.pack(pady=(0, 10))  # Oben platzieren

            # Bild links
            icon_label = tk.Label(top_row, image=photo, bg=color)
            icon_label.pack(side="left", padx=10)

            # Name rechts daneben
            label = tk.Label(top_row, text=f"{name}", font=(
                "Helvetica", 20, "bold"), bg=color)
            label.pack(side="left", padx=10)

            money_value = locale.format_string(
                "%d", player.get_money(), grouping=True)
            money_label = tk.Label(player_frame, text=f"Money: {money_value} $", font=(
                "Helvetica", 18, "bold"), bg=color)
            money_label.pack(pady=3)

            temp_money_label = tk.Label(player_frame, font=(
                "Helvetica", 14, "bold"), bg=color)
            temp_money_label.pack(pady=2)
            player.temp_money_label = temp_money_label
            player.delta_label = temp_money_label

            add_money_entry = tk.Entry(player_frame, font=("Helvetica", 12))
            add_money_entry.pack(pady=2)
            add_money_button = tk.Button(player_frame, text="Add Money", font=("Helvetica", 12),
                                         command=lambda p=player, e=add_money_entry, ml=money_label: self.add_money(p, e, ml))
            add_money_button.pack(pady=5)

            empty_label = tk.Label(player_frame, bg=color)
            empty_label.pack(pady=2)

            spend_money_entry = tk.Entry(player_frame, font=("Helvetica", 12))
            spend_money_entry.pack(pady=2)
            spend_money_button = tk.Button(player_frame, text="Spend Money", font=("Helvetica", 12),
                                           command=lambda p=player, e=spend_money_entry, ml=money_label: self.spend_money(p, e, ml))
            spend_money_button.pack(pady=5)

            empty_label = tk.Label(player_frame, bg=color)
            empty_label.pack(pady=2)

            miete_label = tk.Label(
                player_frame, text="Select Player & Amount $:", font=("Helvetica", 12), bg=color)
            miete_label.pack(pady=2)

            other_player_names = [
                p_name for p_name in self.player_names if p_name != name]
            miete_var = tk.StringVar()
            miete_var.set(other_player_names[0] if other_player_names else "")
            miete_menu = ttk.Combobox(
                player_frame, textvariable=miete_var, values=other_player_names)
            miete_menu.pack(pady=2)
            player.miete_menu = miete_menu

            miete_amount_entry = tk.Entry(player_frame, font=("Helvetica", 12))
            miete_amount_entry.pack(pady=2)

            miete_button = tk.Button(player_frame, text="Pay Rent", font=("Helvetica", 12),
                                     command=lambda payer=player, menu=miete_menu, amount=miete_amount_entry, ml=money_label:
                                     self.pay_rent(payer, menu, amount, ml))
            miete_button.pack(pady=5)

            empty_label = tk.Label(player_frame, bg=color)
            empty_label.pack(pady=2)

            arrow_img_path = resource_path(
                os.path.join("images", "go_arrow.png"))
            try:
                arrow_image = Image.open(arrow_img_path).resize(
                    (80, 80), Image.Resampling.LANCZOS)
                arrow_photo = ImageTk.PhotoImage(arrow_image)
            except FileNotFoundError:
                arrow_photo = None
            self.figure_images.append(arrow_photo)

            los_button = tk.Button(player_frame, image=arrow_photo,
                                   command=lambda p=player, ml=money_label: self.run_los(
                                       p, ml),
                                   bg=color, relief="flat")
            los_button.pack(pady=5)

            player.money_label = money_label
            player.status_label = tk.Label(player_frame, text="Active", font=(
                "Helvetica", 16, "bold"), fg="green", bg=color)
            player.status_label.pack(pady=10)

    def on_player_window_close(self, player, window):
        Player.player_count -= 1
        Player.used_names.remove(player.name)
        self.players.remove(player)
        window.destroy()

    def update_all_rent_menus(self):
        active_names = [p.name for p in self.players if p.is_active]
        for player in self.players:
            if hasattr(player, "miete_menu"):
                other_names = [n for n in active_names if n != player.name]
                player.miete_menu["values"] = other_names
                if other_names:
                    player.miete_menu.set(other_names[0])
                else:
                    player.miete_menu.set("")

    def add_money(self, player, entry, money_label):
        if player.is_active:
            amount = self.check_amount_input(entry)
            if amount is not None:
                player.add_money(amount)
                self.update_money_label(player, money_label)
                self.show_money_delta(player, amount)
            entry.delete(0, tk.END)

    def spend_money(self, player, entry, money_label):
        if player.is_active:
            amount = self.check_amount_input(entry)
            if amount is not None:
                player.spend_money(amount)
                self.update_money_label(player, money_label)
                self.show_money_delta(player, -amount)
                self.update_player_status(player)
                entry.delete(0, tk.END)

    def update_player_status(self, player):
        if player.get_money() < 0:
            player.status_label.config(text="Out of Game", fg="red")
            player.is_active = False
            player.remove_player()
            self.update_all_rent_menus()

            if self.get_active_players_count() == 1:
                winner = self.get_active_players()[0]
                winner.status_label.config(text="Winner!", fg="green")

    def remove_player_from_game(self, player):
        # Entferne den Spieler aus self.players
        self.players.remove(player)
        self.player_names.remove(player.name)
        player_frame = player.temp_money_label.master
        player_frame.destroy()

    def check_amount_input(self, entry):
        value = entry.get().strip()
        if not value:
            self.show_error("Please enter an amount.")
            return None
        try:
            amount = int(value)
            if amount <= 0:
                self.show_error("Amount must be greater than 0.")
                return None
            self.hide_error()
            return amount
        except ValueError:
            self.show_error("Please enter a valid number.")
            return None

    def run_los(self, player, money_label):
        if player.is_active:
            try:
                player.los()
                self.update_money_label(player, money_label)
                self.show_money_delta(player, self.go_bonus)
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
                                self.update_money_label(payer, money_label)
                                self.show_money_delta(payer, -amount)
                                amount_entry.delete(0, tk.END)
                                self.update_money_label(
                                    recipient, recipient.money_label)
                                self.show_money_delta(recipient, amount)
                                self.hide_error()
                                return
                            else:
                                # Überweise verbleibendes Geld an den Empfänger und ändere den Status des Payers
                                last_payer_money = payer.get_money()
                                recipient.add_money(payer.get_money())
                                payer.spend_money(payer.get_money() + 1)
                                self.update_money_label(payer, money_label)
                                self.show_money_delta(
                                    payer,  payer.get_money())
                                amount_entry.delete(0, tk.END)
                                self.update_player_status(payer)
                                payer.is_active = False
                                # Aktualisiere auch das GUI des Empfängers
                                self.update_money_label(
                                    recipient, recipient.money_label)
                                self.show_money_delta(
                                    recipient, last_payer_money)
                                payer.remove_player()
                                # Ändere die Farbe des Geldbetrags, um den Verlust anzuzeigen
                                money_label.config(fg="red")
                                self.hide_error()
                                return
            except ValueError:
                pass

        self.show_error("Invalid rent payment.")

    def show_money_delta(self, player, amount):
        label = player.temp_money_label

        if amount == 0:
            label.config(text="", fg=player.money_label.cget("fg"))
            return

        sign = "+" if amount > 0 else "-"
        color = "green" if amount > 0 else "red"
        label.config(text=f"{sign}{abs(amount):,} $".replace(
            ",", "."), fg=color)
        label.after(2000, lambda: label.config(text=""))

    def show_error(self, message):
        # Wenn das Fehler-Label nicht existiert oder zerstört wurde, erstelle es neu
        if not hasattr(self, 'error_message') or not self.error_message.winfo_exists():
            self.error_message = tk.Label(
                self.root, text="", font=("Helvetica", 16), fg="red")
            # Verwende grid() statt pack()
            self.error_message.grid(row=99, column=0, columnspan=2, pady=10)

        self.error_message.config(text=message)

    def hide_error(self):
        if self.error_message and self.error_message.winfo_exists():
            self.error_message.grid_remove()

    def update_money_label(self, player, money_label):
        money_value = locale.format_string(
            "%d", player.get_money(), grouping=True)
        money_label.config(text=f"Money: {money_value}$")

    def get_active_players(self):
        return [player for player in self.players if player.is_active]

    def get_active_players_count(self):
        return len(self.get_active_players())

    def random_color(self):
        return "#{:02x}{:02x}{:02x}".format(
            random.randint(128, 255),  # R
            random.randint(128, 255),  # G
            random.randint(128, 255)   # B
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerSetupGUI(root)
    root.mainloop()
