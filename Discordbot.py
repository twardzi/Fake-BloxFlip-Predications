import customtkinter as ctk
import discord
import random
import threading
import os
from discord.ext import commands

# Set the appearance and theme for the interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Path to the file with bot info
info_file = "discordbotinfo.txt"

# Function to start the bot
def start_bot(token, server_id):
    intents = discord.Intents.default()
    intents.messages = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')
        # Register slash commands
        guild = discord.Object(id=server_id)
        await bot.tree.sync(guild=guild)

    @bot.tree.command(name="mines", description="Generate a mines field", guild=discord.Object(id=server_id))
    async def mines(interaction: discord.Interaction):
        def generate_mines_field():
            field = []
            for _ in range(5):
                row = []
                for _ in range(5):
                    if random.random() < 0.4:
                        row.append("⭐")
                    else:
                        row.append("💣")
                field.append(row)
            return field
        
        field = generate_mines_field()
        field_str = "\n".join("".join(row) for row in field)
        success_rate = random.randint(0, 100)
        embed = discord.Embed(title="Predictions:", description=f"```\n{field_str}\n```\nPrediction success rate: {success_rate}%", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="roulette", description="Play a game of roulette", guild=discord.Object(id=server_id))
    async def roulette(interaction: discord.Interaction):
        colors = ["Yellow", "Red", "Blue"]
        probabilities = [0.2, 0.4, 0.4]  # Yellow: 20%, Red: 40%, Blue: 40%
        result = random.choices(colors, probabilities)[0]
        embed = discord.Embed(title="Roulette Result", description=result, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="crash", description="Generate crash predictions", guild=discord.Object(id=server_id))
    async def crash(interaction: discord.Interaction):
        crash_value = f"{random.uniform(1.00, 10.00):.2f}x"
        embed = discord.Embed(title="Predictions:", description=crash_value, color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    bot.run(token)

# Function to handle start button click
def on_start_button_click():
    token = token_entry.get()
    server_id = server_id_entry.get()
    with open(info_file, "w") as file:
        file.write(f"{token}\n{server_id}")
    threading.Thread(target=start_bot, args=(token, server_id)).start()

# Function to load saved bot info
def load_bot_info():
    if os.path.exists(info_file):
        with open(info_file, "r") as file:
            lines = file.readlines()
            if len(lines) == 2:
                return lines[0].strip(), lines[1].strip()
    return None, None

# Create the main application window
app = ctk.CTk()
app.title("Discord Bot GUI")

# Labels and entry fields for bot token and server ID
ctk.CTkLabel(app, text="Bot Token:").pack(pady=10)
token_entry = ctk.CTkEntry(app, width=400)
token_entry.pack(pady=10)

ctk.CTkLabel(app, text="Server ID:").pack(pady=10)
server_id_entry = ctk.CTkEntry(app, width=400)
server_id_entry.pack(pady=10)

# Start button
start_button = ctk.CTkButton(app, text="Start Bot", command=on_start_button_click)
start_button.pack(pady=20)

# Load saved data if it exists
saved_token, saved_server_id = load_bot_info()
if saved_token and saved_server_id:
    token_entry.insert(0, saved_token)
    server_id_entry.insert(0, saved_server_id)

app.mainloop()
