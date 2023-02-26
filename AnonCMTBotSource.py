# GV - Indicates the date of last update
SourceLastUpdate = "2023/02/26"
# GV - Indicates the current version number of this project
SourceVersionNumber = "v1.5"

f"""
########  ######## ##     ##     ######   ##     ## #### ########  ######## 
##     ## ##       ##     ##    ##    ##  ##     ##  ##  ##     ## ##       
##     ## ##       ##     ##    ##        ##     ##  ##  ##     ## ##       
##     ## ######   ##     ##    ##   #### ##     ##  ##  ##     ## ######   
##     ## ##        ##   ##     ##    ##  ##     ##  ##  ##     ## ##       
##     ## ##         ## ##      ##    ##  ##     ##  ##  ##     ## ##       
########  ########    ###        ######    #######  #### ########  ######## 

Main Code of @AnonCMTBot Telegram Bot.
Running on Python 3.10.6.
Last Update: {SourceLastUpdate}

Structure of the Project:
📂├── SECRETS
📝│   ├── __init__.py     --------------------------> Empty, To make the CONST folder (& the CONSTANTS.py) importable.
📝│   └── CONSTANTS.py    --------------------------> Below are the variables of this file, Read the <Notes> for more information.
➖│                                                   
➖│                                                   BOT_TOKEN = "###"
➖│                                                   API_ID    = 123
➖│                                                   API_HASH  = "###"
➖│                                                
➖│                                                   # + Another dict named FA_captcha_dict
➖│                                                   # Used two curly-brackets to stop treating them as f-string variable
➖│                                                   EN_captcha_dict = {{
➖│                                                       "Key1": {{...}},
➖│                                                       "Key2:  {{...}},
➖│                                                       ⋮
➖│                                                   }}
➖│
📝├── requirements.txt    --------------------------> Requirements of the Project, you can use the script below instead:
➖│                                                   pip install pyrogram==2.0.99 tgcrypto==1.2.5 pytz==2022.7.1 pyromod==2.0
📝├── AnonCMTBotSource.py --------------------------> This file.
📝├── AnonCMTBot.session  --------------------------> Session file made by Pyrogram on the first run.
📝└── Logger.log          --------------------------> Logging the exceptions & errors.

Notes:
▶️ BOT_TOKEN, API_ID & API_HASH are secret credentials & EN_captcha_dict is hidden for security reasons! Showing its key-value pairs can make it vulnerable to security breaches.
└ You can get your own BOT_TOKEN & API_ID, API_HASH from https://t.me/BotFather & https://my.telegram.org/apps.
▶️ Each section is separated by a big text, generated from here: https://www.messletters.com/en/big-text.
└ You can collapse that sections from #region (e.g. search for #region Handlers).
▶️ Each function's beginning is separated by:
# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ function_name
▶️ You can find the Global Variables by searching for:
GV -
▶️ You can separate each Handler to a file using Smart Plugins (https://docs.pyrogram.org/topics/smart-plugins).
└ It's made into one file for ease of transfer and portability.

There are 14 Global Variables, 9 of them are cofigurable:
- SourceLastUpdate
- SourceVersionNumber
- app (Used as Pyrogram Decorator instead of Client)
- MAXBUTTONS
- MAXBROW
- MaxUserAttempts
- MaxUserRounds
- MaxCommentWaitTime
- MaxCaptchaWaitTime

Others are temporary dictionaries:
- UsersTwoRandomCaptcha
- UsersCaptchaState
- UsersCMTDict
- CaptchaTimeOutTasks
"""

# To connect to the Telegram Client, used filters to check the user's requests
from pyrogram import Client, filters
# To instanciate Message & CallbackQuery, build InlineKeyboardButtons
from pyrogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
# To handle Pyrogram's (actually, Telegram!) exceptions
from pyrogram.errors import (
    #FloodWait, UserIsBlocked,
    PeerIdInvalid, ChannelPrivate,
    ChannelInvalid, UsernameNotOccupied,
    MessageNotModified
)
# To determine ChatType 
from pyrogram.enums import ChatType#, MessageMediaType
# Pyromod (monkey-patcher for Pyrogram) & its config
import pyromod
from pyromod import listen, PyromodConfig
# RegEx, used to determine the correct Telegram link
import re
# Get random captcha
import random
# Develop asyncio captcha timeout function
import asyncio
# To get currently running filename, used on cmd_sourcecode
import os
# To capture current directory's contents & show it to the user on cmd_sourcecode
import subprocess

def stopped_handler(identifier, listener):
    print(f"stopped_handler: The listener has been stopped.")
# Run the stopped_handler on stopping the pyromod handler
PyromodConfig.stopped_handler = stopped_handler
# Enable the Pyromod to throw exceptions (like on timeout)
PyromodConfig.throw_exceptions = True

from SECRETS.CONSTANTS import (
    BOT_TOKEN,
    API_ID,
    API_HASH,
    #EN_captcha_dict,
    FA_captcha_dict
)

#region Logging

# Import logging module
import logging
# Import pytz timezone to change timezone of the logging file to Asia/Tehran
from pytz import timezone as pytzTZ
# Import DateTime to change timezone of the logging file to Asia/Tehran
from datetime import datetime as dt

# One-line FGColors (ForeGroundColors) class for printing colored text
FGColors = lambda: None; FGColors.ENDC='\033[0m'; FGColors.BOLD='\033[1m'; FGColors.LightYellow='\033[93m';

# Logging format to be used in .log file
FileLoggingFormat = f"\n{'🔹'*50}\n📅 %(asctime)s.%(msecs)03d 💥%(levelname)s💥 📁 %(filename)s 📝 %(message)s 🔢%(lineno)d"
# Logging dateformat to be used in .log file
LoggingDateFormat = r"%Y/%m/%d %H:%M:%S"
# Set log level
logging.basicConfig(level=logging.INFO)

# Get logger instance to create handlers
logger = logging.getLogger()

# Add StreamHandler with Default Display of Pyhton
StreamLogging = logging.StreamHandler()
logger.addHandler(StreamLogging)
# Display time in Yellow for the StreamLogger
StreamLogging.setFormatter(logging.Formatter(f"{FGColors.LightYellow}[%(asctime)s.%(msecs)03d]{FGColors.ENDC} %(message)s", LoggingDateFormat))
StreamLogging.setLevel(level=logging.INFO)

# Add FileHandler with Preconfigured Display Format
FileLogging = logging.FileHandler(
    filename="Logger.log",
    # mode="w", clears the Logger.log file when you re-run the Python file.
    mode="w",
    encoding="utf-8"
)
logger.addHandler(FileLogging)
FileLogging.setFormatter(logging.Formatter(FileLoggingFormat, LoggingDateFormat))
FileLogging.setLevel(level=logging.WARNING)

# Set your preferred TimeZone to the logger
LoggingTZString = "Asia/Tehran"
logging.Formatter.converter = lambda *args: dt.now(tz=pytzTZ(LoggingTZString)).timetuple()

#endregion Logging

# GV - Assign the Pyrogram's Client to a variable named app
app = Client(
    # Name of .session file (String)
    name="AnonCMTBot",
    # Bot token taken from BotFather (String)
    bot_token=BOT_TOKEN,
    # API ID (Integer)
    # Telegram Desktop api_id for test: 17349
    api_id=API_ID,
    # API Hash (String)
    # Telegram Desktop api_hash for test: 344583e45741c457fe1862106095a5eb
    api_hash=API_HASH,
    # Bold title on Devices section of the developer's Telegram account (String)
    device_model="AnonCMTBot",
    # Small description displayed after device_model on Devices section (String)
    app_version=f"AnonCMTBot {SourceVersionNumber}",
)



'''
########  ########  ######  ########   #######  ##    ##  ######  ########  ######  
##     ## ##       ##    ## ##     ## ##     ## ###   ## ##    ## ##       ##    ## 
##     ## ##       ##       ##     ## ##     ## ####  ## ##       ##       ##       
########  ######    ######  ########  ##     ## ## ## ##  ######  ######    ######  
##   ##   ##             ## ##        ##     ## ##  ####       ## ##             ## 
##    ##  ##       ##    ## ##        ##     ## ##   ### ##    ## ##       ##    ## 
##     ## ########  ######  ##         #######  ##    ##  ######  ########  ######  
'''
#region TextResponses
#! GV - Response messages sent to the user


FA__cmd_start__Intro = '''سلام! لطفاً لینکِ پستی رو که می‌خوای روش کامنت بگذاری، از گروهِ متصل به کانال، ارسال کن
باید به گروه دسترسی داشته باشم (ادمین، من‌و در گروهِ متصل به کانال، ادمین کرده باشه) تا بتونم کامنت‌ت رو ارسال کنم!
من فقط لینک‌های معتبر از گروه رو قبول می‌کنم.
ویدیوی زیر[ ](https://t.me/HydraBots/7)نحوۀ عملکرد ربات رو نشون می‌ده:
'''

FA__cmd_cancel = '''تمام عملیات‌ها لغو شد.
'''

FA__msg_commentit__InMemoryNotCompleted = '''شما کامنتِ ارسال‌نشده دارید! لطفاً اول تکلیف اون رو مشخص کنید یا دستورِ /cancel رو ارسال کنید.
'''

# + ID or Username PlaceHolder (PH = PlaceHolder)
FA__msg_commentit__FakeID = '''مطمئنی لینک‌و از خودت درنیاوردی!؟ چون همچین {IDorUsernamePH} برای کانال یا گروه، تو تلگرام وجود نداره! :/
'''

FA__msg_commentit__ImNotJoined = '''من ادمینِ این کانال یا گروه نیستم و بهش دسترسی ندارم! از ادمین‌ش بخواه من‌و توی گروهِ متصل به کانال‌ش ادمین کنه! :)
'''

FA__msg_commentit__IsChannelMustGP = '''باید لینکِ پست در گروهِ متصل به کانال رو بفرستی نه لینکِ پستِ خودِ کانال رو!
'''

FA__msg_commentit__NoPostYet = '''برای لینکی که فرستادی، هنوز پُستی وجود نداره! نمی‌تونی براش کامنت بگذاری.
'''

FA__msg_commentit__IsServicePostMustRegularPost = '''این پُست یک پیامِ سیستمی محسوب می‌شه! مثل لحظۀ ساخت کانال؛ نمی‌تونی برای این پُست کامنت بگذاری!
'''

FA__msg_commentit__AskComment = '''لطفاً کامنتی که می‌خوای در زیرِ پست درج بشه، ظرف مدتِ ۲ دقیقه ارسال کن، فوروارد هم قبوله!
'''

FA__msg_commentit__SureToCommentOnThis = '''آیا از ارسالِ کامنتی که نوشتی مطمئنی؟
کامنت برای **[این پست]({PostLinkPH})** ارسال میشه.
'''

FA__msg_commentit__AskCommentTimeOut = '''زمانِ ارسال کامنت به پایان رسید، باید مراحل رو از ابتدا شروع کنی! (لینک رو بفرست و...)
'''

FA__AskToResolveCaptcha = '''لطفاً کپچا را حل کنید
(جوابِ موارد زیر را از دکمه‌ها انتخاب کنید):
{CaptchaPH}
'''

FA__CaptchaResponseTimeOut = '''متأسفانه طی مدت زمان لازم برای حل کپچا، پاسخی از سمت شما دریافت نشد و عملیات ارسال کامنت لغو شد.
کپچا باید ظرف کمتر از {MaxCaptchaWaitTimePH} ثانیه حل شود.
می‌توانید مراحل را مجدداً از ابتدا شروع کنید.
'''

FA__cb_resolve_captcha__EndOfCaptchaRounds = '''به‌دلیلِ ورودِ اشتباهِ کپچا بیش از {MaxUserAttemptsPH} دفعه، ارسالِ کامنت لغو شد.
می‌توانید مراحل را مجدداً از ابتدا شروع کنید.
'''

FA__cb_resolve_captcha__WrongAttempt = '''❌ اشتباهه! {RemainingAttemptsPH} دفعه دیگه می‌تونی امتحان کنی.
'''

FA__cb_resolve_captcha__NewCaptchaRound = '''⚠️ کپچا ریسِت شد! اگر این هم درست جواب ندی، باید مجدداً مراحل رو تکرار کنی. لطفاً با دقت جواب بده.
'''

FA__cb_send_comment__CommentSentSuccess = '''کامنتِ شما با موفقیت ارسال شد.
'''

FA__cb_cancel_comment__CommentSentCanceled = '''ارسالِ کامنت لغو شد.
'''

FA__msg_any__SendValidLink = '''پیامت نامعتبر بود! باید لینکِ پستی رو که می‌خوای روش کامنت بذاری، از گروهِ بحث، کپی و ارسال کنی.
'''

FA__cmd_about__FirstPage = '''سلام! خب، قبل از هر چیز، یکم راجع‌به ربات توضیح بدم...
این ربات، کاملاً متن‌باز (Open Source) هست و بدونِ پایگاه داده نوشته شده! لااقل تا نسخۀ 1.5، اگر تغییراتی ایجاد بشه همین‌جا مطلع خواهید شد.
این یعنی هیچ اطلاعاتی از کاربران ذخیره نمیشه و آی‌دیِ عددی هم به‌محضِ ارسال کامنت یا لغو اون، از حافظۀ فَرّار (RAM) حذف میشه؛ به‌همین دلیل هم امکانِ بلاک کردن کاربرانی که براتون کامنت ارسال می‌کنن، وجود نداره.
پس اگر ادمین هستید یا عضوِ یک کانال/گروه، لطفاً در استفادۀ درست و انسانی از ربات، کوشا باشید! :)))
وَ البته:
Don't shoot the messenger!
سایر حَرّافی‌ها و لینکِ نذوراتِ رمزارزی رو می‌تونی با لمسِ دکمه‌های زیر ببینی.
'''

FA__cbs_cmd_about__TermsOfService = '''**📏 شرایط استفاده**

◽️ ربات‌ها فقط درصورتی‌که در گروه، ادمین باشند، امکانِ ارسال پیام رو خواهند داشت. این ربات به هیچ پیامی دسترسی نداره و درکل، عملکردِ خارج از چتِ خودش براش تعریف نشده.
◽️ ربات به‌تنهایی قادر به ارسال پیام نیست؛ هر پیامی که دریافت کنید از یک کاربرِ دیگه که لینکِ گروهِ شما رو داره، ارسال شده.
حتی کاربرانی که در گروهِ شما حضور ندارند امّا از این‌که ربات رو به گروه اضافه کردید، اطلاع دارند و لینکی از گروهِ شما رو دارند، می‌تونن پیام ارسال کنن!
◽️ کُدهای کپچا و نحوۀ نمایش‌شون ممکنه بعدها به‌روز و پیچیده‌تر بشن.
◽️ این پروژه همیشه متن‌باز خواهد موند امّا --ممکنه-- بسته به نیازِ کاربران، در آینده یک پایگاه دادۀ رمزگذاری‌شده بهش اضافه بشه؛ تمامِ مراحلِ توسعۀ این پروژه به اطلاعِ شما خواهد رسید.
'''

FA__cbs_cmd_about__ContactDev = '''بقیه ربات‌هام:
@JSONiceBot
@ChatGPTPortalBot (Not Ready, Under Development)

اگر سؤالی - پیشنهادی - گزارش باگ و لَگی چیزی بود در خدمتم :)
فقط از این ربات انتظار زیادی نداشته باشید! در اوقات فراغتم نوشتمش و در همون اوقات، توسعه پیدا خواهد کرد! 😁
'''

FA__cbs_cmd_about__Donations = '''آدرسِ کیف پولِ رمزارزهام هستن :)
کمک‌های شما مزیدِ امتنان و خستگی‌درکننده خواهد بود 😁

**Bitcoin (BTC)**
`bc1qrvmq85g9datj77y93qk5xncjvgel5upzy8zdck`

**Ethereum (ETH)**
`0x9FFAcc5f37083Db0b843da621107380B06a378D2`

**Dogecoin (DOGE)**
`DNR8byq6GMVs2FCi6HZtXzAiJiwd3cL7Ji`

**TONCOIN (TON) [BEP20]**
`0x9FFAcc5f37083Db0b843da621107380B06a378D2`

**Algo (ALGO)**
`QVUE3SU5IWMCDVULCCJJ2ISPE3TT3JTKP7YBBDHFECHSOH6AYFRAJZAPQY`

**Tron (TRX)**
`TUFPSztqR43rUii1bBwEmfrjVfoHvbfwha`

**Stellar (XLM)**
`GAZXCPN343JQIJ6UPRO5DHHQLEWOMYNATHQQA24OGNOFXCYMKTLLAX7W`

**Tether (USDT) [BEP20]**
`0x9FFAcc5f37083Db0b843da621107380B06a378D2`
'''

FAEN__cmd_about = '''[👨🏻‍💻 AλI](https://t.me/HydraElit)
`© 2023`

**☕ Crypto Donation**:

**Bitcoin (BTC)**
`bc1qrvmq85g9datj77y93qk5xncjvgel5upzy8zdck`

**Ethereum (ETH)**
`0x9FFAcc5f37083Db0b843da621107380B06a378D2`

**Dogecoin (DOGE)**
`DNR8byq6GMVs2FCi6HZtXzAiJiwd3cL7Ji`

**TONCOIN [BEP20]**
`0x9FFAcc5f37083Db0b843da621107380B06a378D2`

**Algo (ALGO)**
`QVUE3SU5IWMCDVULCCJJ2ISPE3TT3JTKP7YBBDHFECHSOH6AYFRAJZAPQY`

**Tron (TRX)**
`TUFPSztqR43rUii1bBwEmfrjVfoHvbfwha`

**Stellar (XLM)**
`GAZXCPN343JQIJ6UPRO5DHHQLEWOMYNATHQQA24OGNOFXCYMKTLLAX7W`
'''
#endregion


'''
##     ## ######## ##       ########  ######## ########   ######  
##     ## ##       ##       ##     ## ##       ##     ## ##    ## 
##     ## ##       ##       ##     ## ##       ##     ## ##       
######### ######   ##       ########  ######   ########   ######  
##     ## ##       ##       ##        ##       ##   ##         ## 
##     ## ##       ##       ##        ##       ##    ##  ##    ## 
##     ## ######## ######## ##        ######## ##     ##  ######  
'''
#region Helpers

# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ pyrogram_captcha_generator

# GV - How many buttons do you want to generate?
MAXBUTTONS = 9
# GV - How many buttons on each row? MaxButtons on each ROW
MAXBROW = 3
'''
MAXBUTTONS = 9 & MAXBROW = 3 Will generate buttons like:
⏹️⏹️⏹️
⏹️⏹️⏹️
⏹️⏹️⏹️
'''
# GV - {UserID: {"ck1": "cv1", "ck2": "cv2"}}
UsersTwoRandomCaptcha = dict()
# GV - Maximum number of wrong_attempts, if user's wrong_attempts reaches this number, sending comment will be terminated
MaxUserAttempts = 3
# GV - Maximum number of rounds before termination (not sending the comment due to incorrect captcha)
MaxUserRounds = 2
# GV - Store user's captcha state on the dictionary
# {UserID: [success_attemps, wrong_attempts, current_round]}
# Will be cleaned after user's timeout on helper_disable_captcha_buttons using helper_cancel
UsersCaptchaState = dict()

async def pyrogram_captcha_generator(UserID: int):

    '''
    Generates random captcha buttons for the given user.

    ### Parameters:
        `UserID` (int): Unique numeric ID of the user.
    ### Returns:
        `[0]` = `final_two_random`: The dictionary of two random emojis/definitions that user's input should be checked with these to see if the choosen button is correct or not (Stored in `UsersTwoRandomCaptcha` GV).

        `[1]` = `finalreply_markup`: The buttons that user should press the correct value.

        `[2]` = `finaltext`: The final text to guide the user.
    '''

    # Get a random key from the English captcha dictionary
    random_captcha_key = random.choice(list(FA_captcha_dict.keys()))
    # Access the corresponding value using the key
    random_captcha_dict = FA_captcha_dict[random_captcha_key]

    # Generate a list of random emoji characters with the len of MAXBUTTONS
    random_emojis = random.sample(list(random_captcha_dict.values()), MAXBUTTONS)
    #print(random_emojis)
    # Generate definitions according to the random emojis
    random_definitions = [list(random_captcha_dict.keys())[list(random_captcha_dict.values()).index(e)] for e in random_emojis]
    #print(random_definitions)

    # Get two random emoji with its definition
    two_random_dict = dict()
    # Get two random indexes to get the emojis that will be displayed to the user to select
    # As we always get random order of emojis, we can use first and fifth emoji
    # Store emojis as key:value on two_random dictionary
    two_random_dict[random_definitions[0]] = random_emojis[0]
    two_random_dict[random_definitions[5]] = random_emojis[5]
    #print(two_random_dict)
    # Store keys (definitions) for display
    final_two_random = f"⬜ **{list(two_random_dict.keys())[0]}**\n⬜ **{list(two_random_dict.keys())[1]}**"
    #print(final_two_random)

    keyboard = list()
    for i in range(0, MAXBUTTONS, MAXBROW):
        row = list()
        for j in range(MAXBROW):
            index = i + j
            # Append each button to the row list, with text of emoji and callback of definition
            row.append(InlineKeyboardButton(text=random_emojis[index], callback_data=random_definitions[index]))
        keyboard.append(row)

    finalreply_markup = InlineKeyboardMarkup(keyboard)
    #print(finalreply_markup)

    # Add two_random_dict to the user's dictionary in UsersTwoRandomCaptcha
    UsersTwoRandomCaptcha[UserID] = two_random_dict

    #finaltext = f"Click on the emojis with the following definitions:\n{final_two_random}"
    finaltext = f"{final_two_random}"
    #print(finaltext)

    return (final_two_random, finalreply_markup, finaltext)


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ helper_msg_commentit

# GV - Temporarily store the user's comment to send on confirmation
# {UserID: [pyrogram.types.Message(Comment)]}
UsersCMTDict = dict()
# GV - Maximum SECONDS that user can send the comment before termination
MaxCommentWaitTime = 120

async def helper_msg_commentit(CI, MI, ChID, MsgID, PrvOPub):

    '''
    Checks the possible errors and if not any error occurred, sends the comment.

    ### Parameters:
        `CI` (client): Client Instance.
        `MI` (message): Message Instance.
        `ChID` (str): Destination ChatID, can be Username too (Discussion Group or Channel).
        `MsgID` (int): ID of the Message that the user wants to reply to.
        `PrvOPub` (str): Should be one of `Prv` or `Pub` (`if isPubORPrv.startswith("c/"):` is `Prv`).
    '''

    ChatID = None

    if PrvOPub == "Prv":
        # Get the exact ChatID by removing c/ & adding -100 at the beginning
        ChatID = int(f"-100{ChID[2:-1]}")
    else:
        # Get username by removing / at the end
        ChatID = ChID[:-1]

    try:
        # Resolve the peer to make sure the bot has access to the discussion group
        resolveit = await CI.resolve_peer(ChatID)
        # Get chat details
        PrvCHorGP = await CI.get_chat(ChatID)
    
    # The channel is Private and the bot is not Admin
    except (ChannelPrivate, ChannelInvalid) as PrvCHorGPNotAdminErr:
        await MI.reply_text(
            text=FA__msg_commentit__ImNotJoined
        )
        #logging.exception(f"PrivateChannelNotAdmin\n{PrvCHorGPNotAdminErr}")
        return "PrivateChannelNotAdmin"

    # Exception raises when the ID or Username is not valid or not occupied
    except (ValueError, UsernameNotOccupied, PeerIdInvalid) as ValErrNotValid:
        if PrvOPub == "Prv":
            # If exception happened, notify the user that the given link's ID is wrong
            await MI.reply_text(
                text=FA__msg_commentit__FakeID.format(IDorUsernamePH="آی‌دی‌ای")
            )
        else:
            # If exception happened, notify the user that the given link's Username is wrong
            await MI.reply_text(
                text=FA__msg_commentit__FakeID.format(IDorUsernamePH="یوزرنیمی")
            )
        #logging.exception(f"IDisWrong\n{ValErrNotValid}")
        return "IDisWrong"
    
    # If chat was a channel, notify the user that it must be discussion group!
    if PrvCHorGP.type == ChatType.CHANNEL:
        await MI.reply_text(
            text=FA__msg_commentit__IsChannelMustGP
        )
    elif PrvCHorGP.type == ChatType.SUPERGROUP:
        # Get message that the user wants to write comment on it
        PrvGPMSGID = await CI.get_messages(ChatID, MsgID)
        # If the message has empty attribute, notify the user that (S)He can't write comment on it
        if PrvGPMSGID.empty == True:
            await MI.reply_text(
                text=FA__msg_commentit__NoPostYet
            )
            return "IDisWrong"
        # If the message has service attribute, notify the user that (S)He can't write comment on it
        elif PrvGPMSGID.service:
            await MI.reply_text(
                text=FA__msg_commentit__IsServicePostMustRegularPost
            )
            return "IDisWrong"
        
            
        # Ask the user to send message so I can comment it
        # We're using pyromod's .listen instead of .ask to make it possible to edit the message after timeout
        AskForCommentMsg = await MI.reply_text(
            text=FA__msg_commentit__AskComment,
            disable_web_page_preview=True,
        )
        try:
            # We're using pyromod's .listen instead of .ask to make it possible to edit the message after timeout
            AskForComment = await CI.listen(
                identifier=(
                    MI.chat.id,
                    MI.from_user.id,
                    None
                ),
                timeout=MaxCommentWaitTime
            )
            # If user sent the command /cancel instead of comment, cancel the operation
            if AskForComment.text == "/cancel":
                await AskForCommentMsg.edit_text(
                    text=FA__cb_cancel_comment__CommentSentCanceled
                )
                await helper_cancel(UserID=MI.from_user.id)
                return "UserCanceledBeforeCommenting"
            
            # Add Comment, DestinationCharID, ReplyToMsgID to the user's dictionary in UsersCMTDict
            UsersCMTDict[MI.from_user.id] = [AskForComment, ChatID, MsgID]
            # Send message with two buttons to post the comment (after completing captcha) or cancel
            AreYouSureToComment = await MI.reply_text(
                reply_to_message_id=AskForComment.id,
                text=FA__msg_commentit__SureToCommentOnThis.format(PostLinkPH=MI.text),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="❌ پشیمون شدم!",
                                callback_data=f"CancelSendingCMT"
                            ),
                            InlineKeyboardButton(
                                text="✅ ارسالِ کامنت",
                                callback_data=f"ConfirmSendingCMT"
                            ),
                        ],

                    ]
                )
            )
            # If the user didn't respond for MaxCommentWaitTime*2, terminate the operation
            await AreYouSureToComment.wait_for_click(
                from_user_id=MI.from_user.id,
                timeout=MaxCommentWaitTime
            )
            # Add sent message's ID to the list so we can remove buttons on command /cancel
            (UsersCMTDict[MI.from_user.id]).append(AreYouSureToComment.id)
        except pyromod.listen.ListenerTimeout:
            await AskForCommentMsg.edit_text(
                text=FA__msg_commentit__AskCommentTimeOut
            )

            return "PyromodTimeout"


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ helper_cancel

async def helper_cancel(UserID: int):

    '''
    Takes UserID & cleans all the dictionaries to allow the user to cancel the current operation and send another comment.
    '''
    
    try:
        # Delete the user's ID from the dictionary which contains:
        # [comment_message, destination_chat_id, reply_message_id]
        del UsersCMTDict[UserID]
        # Delete the previous UsersTwoRandomCaptcha
        del UsersTwoRandomCaptcha[UserID]
        # Delete the previous UsersCaptchaState
        del UsersCaptchaState[UserID]
    except KeyError as KErr:
        pass


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ helper_disable_captcha_buttons

# GV - Maximum SECONDS that user can send the first response to the captcha buttons before termination
MaxCaptchaWaitTime = 60

# GV - Stores the asyncio state of the captcha message for each user
CaptchaTimeOutTasks = dict()

async def helper_disable_captcha_buttons(MI, UserID: int, timeout: int = MaxCaptchaWaitTime):

    '''
    Sleeps for timeout (in seconds), then edits the related message that contains captcha, can be run through `start_disable_captcha_buttons`.

    ### Parameters:
        `MI` (message): Message Instance, the captcha message that you want to edit after timeout.
        `UserID` (int): Unique numeric ID of the User that the captcha buttons sent to.
        `timeout` (int): Timeout in seconds. default to 60 seconds.
    '''

    # Sleep for the amount of timeout
    await asyncio.sleep(timeout)

    try:
        # Edit the message and disable the captcha
        await MI.edit_text(
            text=FA__CaptchaResponseTimeOut.format(MaxCaptchaWaitTimePH=MaxCaptchaWaitTime)
        )
    except MessageNotModified as MNMErr:
        pass

    # Mark the task as completed
    (CaptchaTimeOutTasks[UserID]).completed = True

    # Delete the UserID from the related dictionary
    del CaptchaTimeOutTasks[UserID]

    await helper_cancel(UserID=UserID)


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ start_disable_captcha_buttons

async def start_disable_captcha_buttons(MI, UserID: int, timeout: int = MaxCaptchaWaitTime):

    '''
    Starts the time disable_captcha_buttons counter timer right after the captcha has been sent to the user.

    ### Parameters:
        `MI` (message): Message Instance, the captcha message that you want to edit after timeout.
        `UserID` (int): Unique numeric ID of the User that the captcha buttons sent to.
        `timeout` (int): Timeout in seconds. default to 60 seconds.
    '''

    # Create task to disable buttons after timeout seconds
    usertask = asyncio.create_task(
        helper_disable_captcha_buttons(MI, UserID)
    )
    # Store the usertask on the dictionary so it can be stopped
    CaptchaTimeOutTasks[UserID] = usertask


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ stop_disable_captcha_buttons

async def stop_disable_captcha_buttons(UserID: int):

    '''
    Cancel the task of disabling the captcha buttons for this user as (S)He successfully solved captcha.

    ### Parameters:
        `UserID` (int): Unique numeric ID of the User. 
    '''

    # Check if UserID is in the dictionary
    if UserID in CaptchaTimeOutTasks:
        # Get the usertask from the dictionary
        usertask = CaptchaTimeOutTasks[UserID]
        # Cancel the asyncio task from running (stop disable_captcha_buttons)
        usertask.cancel()
        # Delete the UserID from the related dictionary
        del CaptchaTimeOutTasks[UserID]

#endregion Helpers

'''
##     ##    ###    ##    ## ########  ##       ######## ########   ######  
##     ##   ## ##   ###   ## ##     ## ##       ##       ##     ## ##    ## 
##     ##  ##   ##  ####  ## ##     ## ##       ##       ##     ## ##       
######### ##     ## ## ## ## ##     ## ##       ######   ########   ######  
##     ## ######### ##  #### ##     ## ##       ##       ##   ##         ## 
##     ## ##     ## ##   ### ##     ## ##       ##       ##    ##  ##    ## 
##     ## ##     ## ##    ## ########  ######## ######## ##     ##  ######  
'''
#region Handlers

# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cmd_start

# Run this function only when the user sends message to the bot and message is /start
@app.on_message(filters.private & filters.command(["start"]))
async def cmd_start(client: Client, m: Message):

    # Send introduction message to the user, disable_web_page_preview
    # to make the introduction video's preview visible 
    await m.reply_text(
        text=FA__cmd_start__Intro,
        disable_web_page_preview=False
    )


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cmd_cancel

# Run this function only when the user sends message to the bot and message is /cancel
@app.on_message(filters.private & filters.command(["cancel"]))
async def cmd_cancel(client: Client, m: Message):

    # Disable the sent InlineKeyboardButton
    await client.edit_message_reply_markup(
        chat_id=m.chat.id,
        message_id=int((UsersCMTDict[m.from_user.id])[3]),
        reply_markup=[]
    )

    await helper_cancel(UserID=m.from_user.id)

    # Cancel the listener for this chat
    #client.cancel_listener(chat_id=m.chat.id)
    await m.reply_text(
        text=FA__cmd_cancel
    )


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cmd_about

# Run this function only when the user sends message to the bot and message is /about
@app.on_message(filters.private & filters.command(["about"]))
async def cmd_about(client: Client, m: Message):

    AboutButtons = [
        [
            InlineKeyboardButton(
                text="📏 شرایط استفاده",
                callback_data="TermsOfService"
            ),
        ],
        [
            InlineKeyboardButton(
                text="👨🏻‍💻 ارتباط با توسعه‌دهنده",
                callback_data="BotDevInfo"
            ),
        ],
        [
            InlineKeyboardButton(
                text="☕ خیرات و نذورات :D",
                callback_data="Donations"
            )
        ]
    ]
    
    await m.reply_text(
        text=FA__cmd_about__FirstPage,
        reply_markup=InlineKeyboardMarkup(AboutButtons),
        disable_web_page_preview=True
    )


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cbs_cmd_about

# Activates only when the user presses the buttons associated with cmd_about
@app.on_callback_query(
    filters.regex(pattern=r"^TermsOfService$") |
    filters.regex(pattern=r"^BotDevInfo$") |
    filters.regex(pattern=r"^Donations$") |
    filters.regex(pattern=r"^BackToAboutMenu$")
)
async def cbs_cmd_about(client: Client, callback: CallbackQuery):
    
    # TermsOfService
    TOS = re.search(r"^TermsOfService$", callback.data)
    # BotDevInfo
    BDI = re.search(r"^BotDevInfo$", callback.data)
    # Donations
    Donate = re.search(r"^Donations$", callback.data)
    # Back to about menu
    BtAM = re.search(r"^BackToAboutMenu$", callback.data)

    AboutButtons = [
        [
            InlineKeyboardButton(
                text="📏 شرایط استفاده",
                callback_data="TermsOfService"
            ),
        ],
        [
            InlineKeyboardButton(
                text="👨🏻‍💻 ارتباط با توسعه‌دهنده",
                callback_data="BotDevInfo"
            ),
        ],
        [
            InlineKeyboardButton(
                text="☕ خیرات و نذورات :D",
                callback_data="Donations"
            )
        ]
    ]

    # If TOS is not None, callback comes from TermsOfService button
    if TOS is not None:

        await callback.message.edit_text(
            text=FA__cbs_cmd_about__TermsOfService,
            reply_markup=InlineKeyboardMarkup(AboutButtons),
        )

    elif BDI is not None:

        await callback.message.edit_text(
            text=FA__cbs_cmd_about__ContactDev,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="👨🏻‍💻 ارتباط با توسعه‌دهنده",
                            user_id=2055683815
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔙 بازگشت به منوی اصلی",
                            callback_data="BackToAboutMenu"
                        ),
                    ]
                ],
            ),
        )


    elif Donate is not None:

        await callback.message.edit_text(
            text=FA__cbs_cmd_about__Donations,
            reply_markup=InlineKeyboardMarkup(AboutButtons),
        )

    elif BtAM is not None:

        await callback.message.edit_text(
            text=FA__cmd_about__FirstPage,
            reply_markup=InlineKeyboardMarkup(AboutButtons),
            disable_web_page_preview=True
        )


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ msg_commentit

# Run this function only when the user sends valid Telegram link of a group or channel
@app.on_message(
    filters.private &
    filters.regex(
        pattern=r"^(https://t.me/)(c/[\d]{,64}/|[\w]{5,32}/)(\d{,10})$"
    )
)
async def msg_commentit(client: Client, m: Message):

    # Check if user has unfinished task before processing his link
    if m.from_user.id in UsersCMTDict:
        # Notify the user that (S)He has an unfinished task (/cancel it!?)
        await m.reply_text(
            text=FA__msg_commentit__InMemoryNotCompleted
        )
        return "UserHasUnfinishedTask"

    '''
    Regex Guide:
    GetRegEx.group(NUM)
    NUM=0 ➡️ Whole Link (e.g. https://t.me/c/1123456789/6498 OR https://t.me/Sample/31)
    1 ➡️ https://t.me/
    2 ➡️ ChatID or ChatUsername: c/1123456789/ OR Sample/
    3 ➡️ PostID: 6498 OR 31
    '''
    GetRegEx = re.search(
        r"^(https://t.me/)(c/[\d]{,64}/|[\w]{5,32}/)(\d{,10})$",
        m.text
    )
    # Get ChatID or ChatUsername
    isPubORPrv = GetRegEx.group(2)
    # Get PostID
    GetMsgID = int(GetRegEx.group(3))

    # If isPubORPrv starts with c/, treat as PrivateChat
    if isPubORPrv.startswith("c/"):

        await helper_msg_commentit(
            CI=client, MI=m,
            ChID=isPubORPrv, MsgID=GetMsgID,
            PrvOPub="Prv"
        )

    # Else, treat as PublicChat
    else:
        
        await helper_msg_commentit(
            CI=client, MI=m,
            ChID=isPubORPrv, MsgID=GetMsgID,
            PrvOPub="Pub"
        )


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cb_send_comment

# Activates only when the user presses the button associated with confirm sending the comment
@app.on_callback_query(filters.regex(pattern=r"^ConfirmSendingCMT$"))
async def cb_send_comment(client: Client, callback: CallbackQuery):

    UserID = callback.from_user.id

    # Retrieve a random captcha
    GetCaptcha = await pyrogram_captcha_generator(UserID=UserID)
    # Send captcha to the user
    FirstRoundCaptcha = await client.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=FA__AskToResolveCaptcha.format(
            CaptchaPH=GetCaptcha[2]
        ),
        reply_markup=GetCaptcha[1]
    )
    await start_disable_captcha_buttons(
        MI=FirstRoundCaptcha, UserID=callback.from_user.id
    )
    """ try:
        # Wait for the user's clicks and timeout after 30 seconds (if user didn't clicked during first 30 seconds)
        # if one click occurred, it does nothing, nevermind! wrote my own asyncio (start_disable_captcha_buttons)
        await FirstRoundCaptcha.wait_for_click(
            from_user_id=callback.from_user.id,
            timeout=MaxCaptchaWaitTime
        )
    except pyromod.listen.ListenerTimeout:
        await FirstRoundCaptcha.edit(
            text=FA__CaptchaResponseTimeOut
        )
        await helper_cancel(UserID=callback.from_user.id) """


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cb_cancel_comment

# Activates only when the user presses the button associated with cancel sending the comment
@app.on_callback_query(filters.regex(pattern=r"^CancelSendingCMT$"))
async def cb_cancel_comment(client: Client, callback: CallbackQuery):

    UserID = callback.from_user.id

    await helper_cancel(UserID=UserID)
    
    # Stop the button's loading effect
    await callback.answer()
    # Delete the InlineKeyboardButtons and text to notify the user that operation is terminated
    await client.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=FA__cb_cancel_comment__CommentSentCanceled
    )


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cb_resolve_captcha

# Should come after all on_callback_query that has filters
@app.on_callback_query()
async def cb_resolve_captcha(client: Client, callback: CallbackQuery):

    UserID = callback.from_user.id

    # Data of the captcha button
    CBData = callback.data

    # Get the current text as markdown
    CurrentText = callback.message.text.markdown
    # Get the current reply_markup to preserve the buttons
    CurrentReplyMarkup = callback.message.reply_markup

    # If user not UsersCaptchaState, add the user with default values
    if UserID not in UsersCaptchaState.keys():
        UsersCaptchaState[UserID] = [0, 0, 0]

    # If the answer was correct
    if CBData in UsersTwoRandomCaptcha[UserID].keys():
        # Send a message on top to inform the user that captcha selection was correct
        await callback.answer(f"✅ درسته!")
        # Increase the success_attemps
        UsersCaptchaState[UserID][0] += 1
        # Strikeout the one that has been answered correctly
        NewText = CurrentText.replace(f"⬜ **{CBData}**", f"✅ ~~{CBData}~~")
        try:
            # Edit the message to ✅ the correct captcha
            await callback.message.edit_text(
                text=NewText,
                reply_markup=CurrentReplyMarkup
            )
        except MessageNotModified as MNMErr:
            pass
    else:
        # Increase the wrong_attempts
        UsersCaptchaState[UserID][1] += 1
        wrong_attempts = UsersCaptchaState[UserID][1]
        # Get the remaining_attempts of the user
        remaining_attempts = MaxUserAttempts - wrong_attempts
        # If remaining_attempts was bigger than 0, show the remaining_attempts
        if remaining_attempts > 0:
            #await callback.answer(f"❌ Wrong! {remaining_attempts} attempt{(remaining_attempts > 1)*'s'} remained.", show_alert=True)
            await callback.answer(
                text=FA__cb_resolve_captcha__WrongAttempt.format(
                    RemainingAttemptsPH=remaining_attempts
                ),
                show_alert=True
            )
        
        # Else, increase the current_round and let the user have another captcha
        else:
            # Increase the current_round for this user
            UsersCaptchaState[UserID][2] += 1
            # If the user failed and has current_round < MaxUserRounds, re-generate the captcha
            if UsersCaptchaState[UserID][2] < MaxUserRounds:
                # Delete the previous UsersTwoRandomCaptcha
                del UsersTwoRandomCaptcha[UserID]
                # Reset the previous UsersCaptchaState
                UsersCaptchaState[UserID][0] = 0
                UsersCaptchaState[UserID][1] = 0
                # Disable the previous captcha
                await stop_disable_captcha_buttons(UserID=callback.from_user.id)
                # Get new captcha
                GetCaptcha = await pyrogram_captcha_generator(UserID=UserID)
                # Inform the user that captcha has been reset
                await callback.answer(
                    text=FA__cb_resolve_captcha__NewCaptchaRound,
                    show_alert=True
                )
                # Send new captcha
                NextRoundCaptcha = await client.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=callback.message.id,
                    text=FA__AskToResolveCaptcha.format(
                        CaptchaPH=GetCaptcha[2]
                    ),
                    reply_markup=GetCaptcha[1]
                )
                await start_disable_captcha_buttons(
                    MI=NextRoundCaptcha,
                    UserID=callback.from_user.id
                )

            # Else, if the user didn't pass the captcha and reached MaxUserRounds, Terminate
            else:
                await callback.message.edit_text(
                    text=FA__cb_resolve_captcha__EndOfCaptchaRounds.format(
                        MaxUserAttemptsPH=MaxUserAttempts
                    )
                )
                await helper_cancel(UserID=callback.from_user.id)
                return "EndOfCaptchaRounds-Terminated"
    
    # If the user correctly answered all captcha, send the comment
    if UsersCaptchaState[UserID][0] == len(UsersTwoRandomCaptcha[UserID]):

        await stop_disable_captcha_buttons(
            UserID=callback.from_user.id
        )
        
        # Access the UsersCMTDict data for this user
        MainCMTMsg = (UsersCMTDict[UserID])[0]
        ReplyToThisChatID = (UsersCMTDict[UserID])[1]
        ReplyToThisMsgID = (UsersCMTDict[UserID])[2]

        # Send the comment for the specified destination chat
        Commented = await MainCMTMsg.copy(
            chat_id=ReplyToThisChatID,
            reply_to_message_id=ReplyToThisMsgID
        )

        # Stop the button's loading effect
        await callback.answer()
        # Add a button so that user can see the sent comment
        await client.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.id,
            text=FA__cb_send_comment__CommentSentSuccess,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="مشاهدۀ کامنتِ ارسال‌شده",
                            url=f"{Commented.link}"
                        )
                    ]
                ]
            )
        )
        # Empty the user's dictionary
        await helper_cancel(UserID=UserID)


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ cmd_sourcecode

# Run this function only when the user sends message to the bot and message is /sourcecode
@app.on_message(filters.private & filters.command(["sourcecode"]))
async def cmd_sourcecode(client: Client, m: Message):

    # Run the tree command and capture its output to show the directory that scripts run from it
    tree_output = subprocess.run(['tree'], capture_output=True, text=True)

    # Get currently running file's name
    running_script_filename = os.path.basename(__file__)

    await m.reply_document(
        caption=f"**Updated at**: {SourceLastUpdate}\n**Version**: {SourceVersionNumber}\n\n`{tree_output.stdout}`",
        document=running_script_filename,
        file_name=running_script_filename,
        quote=True
    )


# Func ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙ msg_any

# Run this function only when the user sends an invalid message
# (when function msg_commentit not executed)
@app.on_message(filters.private)
async def msg_any(client: Client, m: Message):
    
    await m.reply_text(
        text=FA__msg_any__SendValidLink
    )

#endregion Handlers

app.run()
