"""
    Config file
"""

"""
Please be sure you haven't slash ('/') at the end of an explorer link,
because in this case a Delegate Monitor tool page can't load a data.
I guess, it's kind of a bug.

Atm you can't check is explorer synchronised or not.
Therefore, for a double-checking uses 2 explorers.
"""
# Tuple of explorers
explorer = (
    'https://explorer.testnet.shiftnrg.org/delegateMonitor',
    'https://testnet.shiftnrg.com.mx/delegateMonitor'
)

"""
Number of active delegates on explorer's delegateMonitor page.
"""
# Delegates to check
active_delegates = 101

"""
Timeout '1' mean if we have a message it will be sent,
but next will be sent only on the 3-rd run of the script.

Workmode:
timeout = 23
script running once in 15 minutes
recurring message will be sent every 6 hours
"""
# Delay for recurring messages
timeout = 23

"""
Please be sure that you type 'True' or 'False' with a capital letter.
Also, it shouldn't have any type of brackets.
"""

"""
'apiKey' - token of your Telegram bot.
'chat_id' - ID of your Telegram chat or channel.

Bot should be an admin of chat or channel for posting messages.
Also, you can recive messages from bot itself by using as a chat_id
your own ID.

You can find your ID or ID of chat or channel by using @get_id_bot bot.
"""
# Telegram bot data for posting messages
telegram = {
    "enabled": False,
    "apiKey": "",
    "chat_id": ""
}

"""
Can be used same bot, but just another chat or channel.
"""
# Telegram bot data for logs
telegram_debug = {
    "enabled": False,
    "apiKey": "",
    "chat_id": ""
}

"""
'projectName' - name of your Ryver project.
'forumID' - ID of your Ryver forum to send messages to.
'login' - login of your bot's account.
'password' - password of your bot's account.

Bot should be added to the forum manually.
"""
# Ryver data for posting messages
ryver = {
    "enabled": False,
    "projectName": "shiftnrg",
    "forumID": "1094320",
    "login": "",
    "password": ""
}
