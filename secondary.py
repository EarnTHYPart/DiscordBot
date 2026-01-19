import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import time
import json
from collections import defaultdict, deque
import requests
from config import BotConfig

# Validate configuration on startup
BotConfig.validate()

baseUrl = "https://api.api-ninjas.com/v1/profanityfilter"

# Setup guild ID from config
GUILD_ID = discord.Object(id=BotConfig.GUILD_ID)

# persistence helpers
def load_strikes():
    if not os.path.exists(BotConfig.STRIKE_FILE):
        try:
            with open(BotConfig.STRIKE_FILE, "w") as f:
                json.dump({}, f)
        except Exception:
            pass
        return {}
    try:
        with open(BotConfig.STRIKE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_strikes(data):
    try:
        with open(BotConfig.STRIKE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

strikes = load_strikes()
message_history = defaultdict(lambda: deque())  # user_id -> deque of timestamps

# ---------------- BOT CLIENT ---------------- #
class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=BotConfig.COMMAND_PREFIX, intents=intents)
        self.synced = False  # Prevent multiple syncs

    async def setup_hook(self):
        # register any persistent views if needed in future
        pass

    async def on_ready(self):
        if not self.synced:
            try:
                await self.tree.sync(guild=GUILD_ID)
            except Exception:
                # fallback to global sync if guild sync fails
                try:
                    await self.tree.sync()
                except Exception:
                    pass
            self.synced = True
        print(f'✅ Logged in as {self.user}!')

    async def on_message(self, message):
        # Basic guards
        if message.author.bot:
            return

        # Print for debugging
        print(f'Message from {message.author} ({message.author.id}) in {getattr(message.channel, "name", "DM")}: {getattr(message, "content", "")}')

        # Profanity check
        content = (message.content or "")
        content_lower = content.lower()
        if any(bw in content_lower for bw in BotConfig.BANNED_WORDS if bw):
            try:
                await message.delete()
            except discord.Forbidden:
                pass
            user_id = str(message.author.id)
            strikes[user_id] = strikes.get(user_id, 0) + 1
            save_strikes(strikes)
            try:
                await message.channel.send(f"{message.author.mention}, that language is not allowed. Strike {strikes[user_id]}/{BotConfig.STRIKES_TO_BAN}.", delete_after=8)
            except Exception:
                pass
            await self.log_mod_action(f"Profanity: {message.author} ({message.author.id}) used banned word in {getattr(message.channel, 'mention', str(message.channel))}. Strike {strikes[user_id]}.")
            if strikes[user_id] >= BotConfig.STRIKES_TO_BAN:
                if message.guild:
                    try:
                        await message.guild.ban(message.author, reason="Exceeded profanity strikes")
                        await self.log_mod_action(f"Banned {message.author} for exceeding profanity strikes.")
                    except Exception as e:
                        await self.log_mod_action(f"Failed to ban {message.author}: {e}")
            return  # stop further processing for this message

        # Spam detection
        now = time.time()
        history = message_history[message.author.id]
        history.append(now)
        # drop old timestamps
        while history and now - history[0] > BotConfig.SPAM_TIME_WINDOW:
            history.popleft()
        if len(history) >= BotConfig.SPAM_MESSAGE_LIMIT:
            # consider spam - attempt to ban (only in guilds)
            try:
                await message.delete()
            except discord.Forbidden:
                pass
            if message.guild:
                try:
                    await message.guild.ban(message.author, reason="Spam detected (automated)")
                    try:
                        await message.channel.send(f"{message.author.mention} has been banned for spamming.", delete_after=8)
                    except Exception:
                        pass
                    await self.log_mod_action(f"Banned {message.author} for spamming ({len(history)} msgs in {BotConfig.SPAM_TIME_WINDOW}s).")
                except Exception as e:
                    await self.log_mod_action(f"Failed to ban {message.author} for spam: {e}")
            else:
                # DM spam or unable to ban: warn and clear history
                try:
                    await message.channel.send("Please stop spamming.", delete_after=8)
                except Exception:
                    pass
            history.clear()
            return

        # simple greeting
        if content.startswith('Hey'):
            try:
                await message.channel.send(f'Hello There {message.author.mention}!')
            except Exception:
                pass

        # allow commands to be processed
        await self.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        try:
            channel = reaction.message.channel if reaction.message else None
            if channel:
                await channel.send(f'{user} reacted with {reaction.emoji}!')
        except Exception:
            pass

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            try:
                await ctx.send("Command not found.")
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send("You don't have permission to run that command.")
            except Exception:
                pass
        else:
            try:
                await ctx.send(f"An error occurred: {str(error)}")
            except Exception:
                pass
            # also log
            try:
                await self.log_mod_action(f"Command error by {getattr(ctx, 'author', 'unknown')}: {error}")
            except Exception:
                pass

    async def log_mod_action(self, message: str):
        if BotConfig.MOD_LOG_CHANNEL_ID:
            try:
                ch = self.get_channel(int(BotConfig.MOD_LOG_CHANNEL_ID))
                if ch:
                    await ch.send(f"[MOD LOG] {message}")
            except Exception:
                pass

client = Client()


# ---------------- SLASH COMMANDS ---------------- #
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

# ---------------- BUTTON UI ---------------- #
class ButtonView(discord.ui.View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.blurple, emoji="😊")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked a button!", ephemeral=True)
    @discord.ui.button(label="2nd Button", style=discord.ButtonStyle.red, emoji="🔥")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You are a good boy", ephemeral=True)
    @discord.ui.button(label="3rd Button", style=discord.ButtonStyle.green, emoji="😘")
    async def button3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You are a QT Pie", ephemeral=True)

@client.tree.command(name="button", description="Display a button", guild=GUILD_ID)
async def button(interaction: discord.Interaction):
    await interaction.response.send_message("Here is a button!", view=ButtonView())


# ---------------- PING ---------------- #
@client.command(name="ping")
async def ping(ctx):
    latency = round(client.latency * 1000)
    try:
        await ctx.send(f'Pong! Latency: {latency}ms')
    except Exception:
        pass

# ---------------- ADMIN / MODERATION COMMANDS ---------------- #
@client.command(name="addrole")
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send("Role not found.")
        return
    try:
        await member.add_roles(role, reason=f"Role added by {ctx.author}")
        await ctx.send(f"Added role {role.name} to {member.mention}.")
        await client.log_mod_action(f"{ctx.author} added role {role.name} to {member}.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to manage that role.")
    except Exception as e:
        await ctx.send(f"Failed to add role: {e}")

@client.command(name="removerole")
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send("Role not found.")
        return
    try:
        await member.remove_roles(role, reason=f"Role removed by {ctx.author}")
        await ctx.send(f"Removed role {role.name} from {member.mention}.")
        await client.log_mod_action(f"{ctx.author} removed role {role.name} from {member}.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to manage that role.")
    except Exception as e:
        await ctx.send(f"Failed to remove role: {e}")

@client.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    try:
        await member.kick(reason=f"{reason} (by {ctx.author})")
        await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")
        await client.log_mod_action(f"{ctx.author} kicked {member}. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to kick: {e}")

@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    try:
        await member.ban(reason=f"{reason} (by {ctx.author})")
        await ctx.send(f"{member.mention} has been banned. Reason: {reason}")
        await client.log_mod_action(f"{ctx.author} banned {member}. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to ban: {e}")

@client.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_tag: str):
    try:
        name, discrim = member_tag.split("#")
    except ValueError:
        await ctx.send("Use the format: username#discriminator")
        return
    try:
        banned = await ctx.guild.bans()
        for ban_entry in banned:
            user = ban_entry.user
            if (user.name, user.discriminator) == (name, discrim):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                await client.log_mod_action(f"{ctx.author} unbanned {user}.")
                return
        await ctx.send("User not found in ban list.")
    except Exception as e:
        await ctx.send(f"Failed to unban: {e}")

@client.command(name="mention")
@commands.has_permissions(administrator=True)
async def mention(ctx, *, target: str):
    # target can be @role or @user mention or plain text
    try:
        await ctx.send(target)
    except Exception:
        pass

# ---------------- Run Bot ---------------- #
if __name__ == "__main__":
    print("Starting Discord Bot with Advanced Moderation...")
    print("Configuration Summary:")
    for key, value in BotConfig.get_summary().items():
        print(f"  {key}: {value}")
    client.run(BotConfig.BOT_TOKEN)
