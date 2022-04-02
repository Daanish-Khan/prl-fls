from email import message
import hikari
import datetime
import random
import re

# Console colours
class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

bot = hikari.GatewayBot(token='')

# Globals
prevtime = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')
vowel_set = ['a', 'e', 'i', 'o', 'u']
special_vowel_set = { 
    'a': ['â', 'à', 'ɑ', 'å', 'ã', 'а', 'ᵃ', 'ạ', 'ª', 'ą'],
    'e': ['é', 'ê', 'è', 'ë'],
    'i': ['î','ì','ï', 'і'],
    'o': ['ô','ò', 'о'],
    'u': ['û', 'ù', 'ü']
}
vowel = 'a'
channel_ids = []

# Channels you want the bot to be active in go here
approved_channel_ids = []  

@bot.listen(hikari.GuildMessageCreateEvent)
async def process_sent_message(event):

    # Check if message is empty or is a bot 
    if event.is_bot or not event.content or not (event.channel_id in approved_channel_ids):
        return

    # Add guild channel to list of channels
    if not any(channel.id == event.get_channel().id for channel in channel_ids):
        channel_ids.append(event.get_channel())
        print(f'{bcolours.WARNING}ADDED CHANNEL ' + event.get_channel().name)

    # Get message from server
    msg = sanitize_msg(event.content)
 
    print(f'{bcolours.HEADER}MESSAGE BY {bcolours.ENDC}' + event.get_member().display_name + f'{bcolours.HEADER} IN {bcolours.ENDC}' + event.get_channel().name + f'{bcolours.HEADER}: {bcolours.ENDC}' + msg)

    # Timeout user if used vowel
    try:
        if message_check(event):
            timeout = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=10)

            await event.get_member().edit(communication_disabled_until=timeout)
            await event.get_channel().send(event.get_member().mention + ' fck y nd yr vwl **' + vowel + '**, mtd fr 10s <:KEKW:773708462529445898>')

            print(f'{bcolours.OKCYAN}TIMED OUT IN {bcolours.ENDC}' + event.get_channel().name + f'{bcolours.OKCYAN}: {bcolours.ENDC}' + event.get_member().display_name)
            await event.message.delete()
    except Exception as e:

        print(e)
        # Fuck mods :(
        print(f'{bcolours.FAIL}CANNOT TIMEOUT MOD {bcolours.ENDC}' + event.get_member().display_name + f'{bcolours.FAIL} IN {bcolours.ENDC}' + event.get_channel().name + f'{bcolours.FAIL}!{bcolours.ENDC}')
        await event.get_channel().send(event.get_member().mention + ' cnt mte y bt fck y nywys <:pepehands:715224075022368769>')
        await event.message.delete()

    # Notifies users which vowel you cant use
    if vowel_picker(event):
        embed = hikari.Embed(
            title='FCK VWLS: ' + vowel.upper(),
            description='FCK TH VWL **' + vowel.upper() + '** N PRTCLR',
            colour="EE3007"
        )

        for channel in channel_ids:
            await channel.send(embed)
    
# Handles message editing
@bot.listen(hikari.GuildMessageUpdateEvent)
async def process_edited_message(event):
    await process_sent_message(event)

def sanitize_msg(msg):
    custom_emotes = re.findall(r'\<.*?\>', msg)

    for emote in custom_emotes:
        msg = msg.replace(emote, "")
    
    msg = re.sub(r'http\S+', '', msg)
    return msg

def vowel_picker(event):
    global prevtime
    global vowel

    fmt = '%H:%M:%S'
    time = event.message.created_at.strftime(fmt)

    # Changes vowel every 2 minutes
    tdelta = datetime.datetime.strptime(time, fmt) - datetime.datetime.strptime(prevtime, fmt)

    if tdelta.seconds > 120:
        vowel = random.choice(vowel_set)
        prevtime = time

        print(f'{bcolours.WARNING}VOWEL CHANGE: {bcolours.ENDC}' + vowel)

        return True
    
    return False
    
def message_check(event):
    emoji_set = ['🇦','🇪','🇮','🇴','🇺','🇾']
    msg = sanitize_msg(event.content)

    # Checks for unicode
    if any(emoji in emoji_set for emoji in msg) or '🅰️' in msg:
        return True

    # Check for vowel
    return vowel in msg.lower() or any(fr_vowel in special_vowel_set[vowel] for fr_vowel in msg.lower())

# Unleash hell
bot.run()