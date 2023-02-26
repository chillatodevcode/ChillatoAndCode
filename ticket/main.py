import asyncio

import discord
from discord.ext import commands
from discord.ui import Button, View
import sqlite3

try:
    conn = sqlite3.connect("ticket.db")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS ticket (openticket INT)")
    conn.commit()
except:
    pass
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    button = Button(label="Crea ticket 📨", style=discord.ButtonStyle.primary)
    button.callback = ticketfunction
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="✉️ TICKET ✉️", description="Hai bisogno di aiuto o hai problemi? bene apri un ticket")
    await client.get_channel(1079276838762856488).send(embed=embed, view=v)
    while True:
        for a, in conn.cursor().execute("SELECT openticket FROM ticket").fetchall():
            conn.cursor().execute("DELETE FROM ticket WHERE openticket = ?", [a])
            conn.commit()
        await asyncio.sleep(86400)

@client.command
@commands.has_role(1076004838699175976)
async def ticket(ctx):
    button = Button(label="Crea ticket 📨", style=discord.ButtonStyle.primary)
    button.callback = ticketfunction
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="✉️ TICKET ✉️", description="Hai bisogno di aiuto o hai problemi? bene apri un ticket")
    embed.set_thumbnail(url="https://png2.cleanpng.com/sh/dec73a4396463148b86eb85c9857cf4f/L0KzQYm3U8E4N6pviZH0aYP2gLBuTfVuaZpxRdV4bYD4hLb5Tflkd594Rd54Z3Awc73wkL1ieqUye9H2cIX3dcO0hb1uaZpxRdV1aYDkgsX6TcViaZVpT6U8NEazR4O7TsU1QGE9SqM6MUW1QYS7UsI2QWM9Tqo3cH7q/kisspng-email-computer-icons-logo-clip-art-computer-e-mail-cliparts-5aadd733460724.5480821115213422592868.png")
    await ctx.send(embed=embed, view=v)

async def ticketfunction(interaction: discord.Interaction):
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name="Moderators")
    dio = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }
    if isOpen(interaction.user.id):
        await interaction.response.send_message("Hai già aperto un ticket aspetta 24 ore", ephemeral=True)
    else:
        closebtn = Button(label="Chiudi ticket 🔐", style=discord.ButtonStyle.red)
        closebtn.callback = close_ticket
        v = View(timeout=None).add_item(closebtn)
        channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-ticket", overwrites=dio)
        ticketcreate = discord.Embed(title="🆘 Benvenuto nel ticket 🆘", description=f"Benvenuto nel tuo ticket ora chiedi quello che devi chiedere gli staff ti risponderanno presto")
        await channel.send(embed=ticketcreate, view=v)
        await interaction.response.send_message(f"Ho creato il tuo ticket con successo", ephemeral=True)
        conn.cursor().execute("INSERT INTO ticket (openticket) VALUES (?)", [interaction.user.id])
        conn.commit()

async def close_ticket(interaction: discord.Interaction):
    if interaction.user.get_role(1076004838699175976) or interaction.user.get_role(1076004838699175976) or interaction.user.get_role(1076004840863453205):
        await interaction.channel.delete()

def isOpen(user_id: int):
    result = conn.cursor().execute("SELECT openticket FROM ticket WHERE openticket = ?", [user_id])
    if len(result.fetchall()) > 0:
        return True
    else:
        return False

client.run("")
