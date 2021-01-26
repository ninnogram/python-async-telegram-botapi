from ninnobotapi import ninnobotapi
import asyncio

#This must be an async function.
#Call it however you want and then pass it in the init function.

async def handler(update={}):
    if "message" in update:
        messageid = update["message"]["message_id"]
        if "text" in update["message"]:
            msg = update["message"]["text"]
        if "caption" in update["message"]:
            msg = update["message"]["caption"]
        chatid = update["message"]["chat"]["id"]
        userid = update["message"]["from"]["id"]
        name = update["message"]["from"]["first_name"]
        mention = f"<a href='tg://user?id={userid}'>{name}</a>"
        if "username" in update["message"]["from"]:
            username = update["message"]["from"]["username"]
        else:
            username = ""
        if msg.startswith("/start"):
            await bot.sendmessage(chat_id=chatid, text=f"Hi {mention}!\nI'm a full-async botapi class developed by <a href='tg://user?id=1006953642'>@Ninno</a>\nCommands: /async, /kb, /webrequest.", parse_mode='html', reply_to_message_id=messageid)
        if msg.startswith("/kb"):
            kb = {"inline_keyboard": [[{"text": "Hi!", "url": "t.me/ninno"}]]}
            await bot.sendmessage(chat_id=chatid, text="Inline keyboard.", reply_markup=kb, reply_to_message=messageid)
        if msg.startswith("/webrequest"):

            message = (await bot.sendmessage(chat_id=chatid, text=f"Wait..."))['message_id']
            my_ip = (await bot.webRequest(url="http://www.randomnumberapi.com/api/v1.0/random", type="get"))[0]
            await bot.editmessagetext(chat_id=chatid, text=f"Random number: {my_ip}", message_id=message)
        if msg.startswith("/async"):
            await bot.sendmessage(chat_id=chatid, text="1")
            await asyncio.sleep(5)
            await bot.sendmessage(chat_id=chatid, text="2")


"""
Parameters:
token = REQUIRED bot token, create a new bot with t.me/botfather
handler_function = required if you want to use getupdates, pass a valid async function with an arg
endpoint = not required, if you have a custom botapi server, please pass the link like 'https://xxx.xxx'
           DEFAULT: https://api.telegram.org/
startup_info = Shows bot info when you start the script
               DEFAULT: False
"""


bot = ninnobotapi(token="1158940416:AAHBU8_B5fvpJ-ThZ1OHChGsGYME", handler_function=handler, startup_info=True) #initializing
bot.startPolling() #start bot updates polling
