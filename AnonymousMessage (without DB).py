"""
This bot Anonymizes the user message and sends it to the Admin.
"""

from pyrogram import Client, filters

import logging
import secrets
from datetime import datetime as dt, timedelta

app = Client(

    session_name = "AnonBot",
    bot_token = "UQHGCEBZ9M1YPVF8J5AXI04L6W23D7SKTONRLS569R030F",

    api_id = 69132890,
    api_hash = "YTZIGNFPWMDBAX2J3O1648VC0RH7QLUK",
    device_model = "AnonMsgBot",
    app_version = "AnonMsgBot v1.0"

    )

# Configure the logging
logging.basicConfig(
    level=logging.INFO,
    filename='./ðâð¨app.log',
    filemode='a+', encoding='utf-8',
    format=f"\n{'ð¹'*25}\nð %(asctime)s ð¥ %(levelname)s ð¥ ð %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
    )

# Global variable AdminID (enter your numeric ID)
AdminID = 123456789
# Global variable date-hash separator (better to include only one character)
DTHSep = 'â'

# Global dictionary to store message_id:user_id as key:value
DataDict = {}
# Global set to store user_id as the Blocked Account
BlockedAccSet = {'init'}


# On user start
@app.on_message(filters.command(["start"]))
async def on_start(c, m):
    await m.reply_text("Hi! ð")


# Get user message and exclude the admin messages from this function
@app.on_message(filters.all & ~filters.user(AdminID))
async def on_user_msg(c, m):

    if m.from_user.id not in BlockedAccSet:
        # Generates a secret as message_id based on message time (Unix) + secret
        # .token_hex(4) - generates a 4*2 = 8 character hexadecimal string
        secretgen = secrets.token_hex(4)
        dtsecret = f"{m.date}{DTHSep}{secretgen}"
        # Store message_id and user_id in dictionary
        DataDict[dtsecret] = m.from_user.id
        # Send message_id to admin
        await app.send_message(AdminID, dtsecret)
        # Send a copy of the message to the admin
        await m.copy(chat_id=AdminID)
    else:
        await m.reply_text("ð¤: âYou are **blocked** from using this bot!\nWork on your personality and behavior.â")


# Activates by admin message only and replies to the user that sent the message
@app.on_message(filters.user(AdminID))
async def on_admin_msg(c, m):

    # Check if Admin is replying to a message
    if m.reply_to_message is not None:

        # Admin should reply to the original message to
        # Get message_id sent before the original message
        retrieve_msg0 = m.reply_to_message.message_id-1
        retrieve_msg1 = await app.get_messages(AdminID, retrieve_msg0)
        OrigKey = retrieve_msg1.text

        if DTHSep not in OrigKey:
            return await m.reply_text("ðð£ð«ðð¡ðð ð¢ðð¨ð¨ððð ððð¥ð¡ð®")

        # Get user_id from the dictionary
        if OrigKey in DataDict:
            # Get user_id (value) from the dictionary
            UserID = DataDict[OrigKey]

            # Block UserID on Admin's command
            if m.text == 'ð¤¬BLOCKð¤¬':
                BlockedAccSet.add(UserID)
                return await m.reply_text(f"ð½ð¡ð¤ðð ðð {UserID}")

            # Send the Admin's message to the user
            await m.copy(chat_id=UserID)
            
            # Get the unix time of the message
            OrigKey2UnixTime = OrigKey.split(DTHSep)[0]
            # Convert it to datetime object
            convertUnix2DT = dt.fromtimestamp(int(OrigKey2UnixTime))
            # Calculate Deletion Time
            # Deletes user from database if the message is too old
            # Get the current time and delete microseconds
            NowTime = dt.now().replace(microsecond=0)
            # timedelta accepts weeks, days, hours, minutes, seconds, and microseconds
            TimeDel = convertUnix2DT+timedelta(days=7)
            print(f"{OrigKey} â will be deleted on: {TimeDel}")

            if NowTime > TimeDel:
                # Delete user from the dictionary
                del DataDict[OrigKey]
                print('ð¥â£ KV Deleted! â£ð¥')

                # Aware the user that it was the last message he received from the Admin
                await app.send_message(UserID,
                f"ð¤: âIt was the last message you received from the Admin, your chatID was deleted on\n**{TimeDel}**.\nSend a new message if you want to continue talking.â")

                return await m.reply_text(
                    f"ð¤: â**ðð© ð¬ðð¨ ð®ð¤ðªð§ ð¡ðð¨ð© ð¢ðð¨ð¨ððð**â\nððð ðððð©ðð¿ ð¬ðð¨ ðð­ð¥ðð§ðð ð¤ð£:\n{str(TimeDel)}")

        else:
            return await m.reply_text("ð¥ **ððððððð¿**! ð¥")
                
    else:
        return await m.reply_text("ðð¤ðª ðððð£'ð© **ððð¥ð¡ð®**!")

        

app.run()
