import discord
from discord.ext import commands
from discord import app_commands
from config import BotConfig

# Validate configuration on startup
BotConfig.validate()

# Setup guild ID
GUILD_ID = discord.Object(id=BotConfig.GUILD_ID)

# ---------------- BOT CLIENT ---------------- #
class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True  
        intents.guilds = True  
        intents.members = True  
        super().__init__(command_prefix="!", intents=intents)
        self.synced = False  # Prevent multiple syncs
        self.colour_role_message_id = None

    async def on_ready(self):
        if not self.synced:
            await self.tree.sync(guild=GUILD_ID)
            self.synced = True
        print(f'✅ Logged in as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author == self.user:
            return
        if message.content.startswith('Hey'):
            await message.channel.send(f'Hello There {message.author.mention}!')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(f'{user} reacted with {reaction.emoji}!')
        if user.bot:
            return
        
        guild = reaction.message.guild
        if not guild:
            return
        
        if hasattr(self, 'colour_role_message_id') and reaction.message.id != self.colour_role_message_id:
            return
        emoji = str(reaction.emoji)
        
        reaction_roles = {
            '🟥': 'Red',
            '🟩': 'Green',
            '🟦': 'Blue',
            '🟨': 'Yellow',
            '🩷': 'Pink'
        }
        
        if emoji in reaction_roles:
            role_name = reaction_roles[emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            if role and user:
                await user.add_roles(role)
                await reaction.message.channel.send(f'{user} has been given the {role_name} role!')
            else:
                await reaction.message.channel.send(f'Role {role_name} not found.')

    async def on_reaction_remove(self, reaction, user):
        await reaction.message.channel.send(f'{user} removed their reaction {reaction.emoji}!')
        if user.bot:
            return

        guild = reaction.message.guild
        if not guild:
            return

        if hasattr(self, 'colour_role_message_id') and reaction.message.id != self.colour_role_message_id:
            return
        emoji = str(reaction.emoji)

        reaction_roles = {
            '🟥': 'Red',
            '🟩': 'Green',
            '🟦': 'Blue',
            '🟨': 'Yellow',
            '🩷': 'Pink'
        }

        if emoji in reaction_roles:
            role_name = reaction_roles[emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            if role and user:
                await user.remove_roles(role)
                await reaction.message.channel.send(f'{user} has been removed from the {role_name} role!')
            else:
                await reaction.message.channel.send(f'Role {role_name} not found.')


client = Client()


# ---------------- SLASH COMMANDS ---------------- #

@client.tree.command(name="colorrole", description="Create a message that lets the users pick color role", guild=GUILD_ID)
async def color_role(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)  
    
    description = (
        "React to the message to become the Power Ranger you want to become:\n"
        "🟥 Red\n"
        "🟩 Green\n"
        "🟦 Blue\n"
        "🟨 Yellow\n"
        "🩷 Pink\n" 
    )

    embed = discord.Embed(
        title="Pick The Color You Want!",
        description=description,
        color=discord.Color.blurple()
    )

    # send the embed in the channel (not ephemeral)
    message = await interaction.channel.send(embed=embed)

    # add reactions
    emojis = ["🟥", "🟩", "🟦", "🟨", "🩷"]
    for emoji in emojis:
        await message.add_reaction(emoji)
        
    client.colour_role_message_id = message.id
    
    await interaction.followup.send("Color role message created successfully!", ephemeral=True) 


@client.tree.command(name="hello", description="Say Hello!", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello {interaction.user.mention}!')


@client.tree.command(name="print", description="Print whatever you say", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)


@client.tree.command(name="embed", description="Embed Demo!", guild=GUILD_ID)
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(
        title="I am a Title",
        url="https://www.reddit.com/r/mushokutensei/",
        description="I am the description",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/mushoku-tensei/images/5/54/Rudeus_Greyrat_Anime.png")
    embed.add_field(name="Field 1", value="This is field 1", inline=False)
    await interaction.response.send_message(embed=embed)


# ---------------- DROPDOWN MENU ---------------- #
class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Option 1", description="This is option 1", emoji="🍎"),
            discord.SelectOption(label="Option 2", description="This is option 2", emoji="🍌"),
            discord.SelectOption(label="Option 3", description="This is option 3", emoji="🍇"),
        ]
        super().__init__(placeholder="Please choose an option", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected: **{self.values[0]}**", ephemeral=True)


class MenuView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Menu())


@client.tree.command(name="menu", description="Display a dropdown menu", guild=GUILD_ID)
async def myMenu(interaction: discord.Interaction):
    await interaction.response.send_message("Here is a menu:", view=MenuView())


# ---------------- RUN BOT ---------------- #
if __name__ == "__main__":
    print("Starting Discord Bot...")
    print("Configuration Summary:")
    for key, value in BotConfig.get_summary().items():
        print(f"  {key}: {value}")
    client.run(BotConfig.BOT_TOKEN)
