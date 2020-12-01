from pyrogram import Client , filters
from pyrogram.raw import functions
from pyrogram.types import Message
from termcolor import colored
from datetime import datetime
from random import choice
import pytz, jdatetime, os
from database import DATA, save

if len(DATA["info-self"]["api_id"]) == 0:
    set_apiid = int(input("send API_ID : "))
    DATA["info-self"]["api_id"].append(set_apiid)
    save()

if len(DATA["info-self"]["api_hash"]) == 0:
    set_apihash = str(input("send API_HASH : "))
    DATA["info-self"]["api_hash"].append(set_apihash)
    save()

if not os.path.exists("txt"):
    os.mkdir("txt")

list_user = DATA["list"]["user"]
api_id = DATA["info-self"]["api_id"][0]
api_hash = DATA["info-self"]["api_hash"][0]
list_color = ["grey","red","green","yellow","blue","magenta","cyan"]
cli = Client("bot", api_id, api_hash)


@cli.on_message(filters.command("help", "") & filters.me)
async def help(client, msg: Message):
    text_help = """
راهنمای ربات :

اضافه کردن یوزر برای ذخیره کردن متن
`useradd` id

حذف یوزر از لیست ذخیره سازی متن
`userrem` id

گرفتن لیست یوزر های ذخیره سازی متن
`userlist`

پاکسازی تمام یوزر های ذخیره سازی متن
`userclean`

ارسال فایل متن های ذخیره شده شخص مورد نظر
`sendfile` id

ارسال تمام فایل های ذخیره شده
`sendfile`

پاک کردن فایل متن دخیره شده یک شخص
`cleanfile` id

پاکسازی تمام فایل متن های ذخیره شده
`cleanfile`
"""
    await msg.edit(text_help)


@cli.on_message(filters.command("useradd", "") & filters.me)
async def useradd(client, msg: Message):
    user = " ".join(msg.command[1:])
    if not user:
        await msg.edit("دستور وارد شده اشتباه است! \n\n شما باید یک مقدار وارد کنید... \n\n `useradd 1346338819`")
        return
    data = DATA["list"]["user"]
    if int(user) in data:
        await msg.edit("این یوزر از قبل اضافه شده است!")
        return
    DATA["list"]["user"].append(int(user))
    save()
    await msg.edit(f"کاربر [{user}](tg://user?id={user}) به لیست اضافه شد")

@cli.on_message(filters.command("userrem", "") & filters.me)
async def userrem(client, msg: Message):
    user = " ".join(msg.command[1:])
    if not user:
        await msg.edit("دستور وارد شده اشتباه است! \n\n شما باید یک مقدار وارد کنید... \n\n `userrem 1346338819`")
        return
    data = DATA["list"]["user"]
    if int(user) in data:
        data.remove(int(user))
        save()
        await msg.edit(f"کاربر [{user}](tg://user?id={user}) از لیست حذف شد")
    else:
        await msg.edit("چنین ایدی وجود ندارد!")
        return

@cli.on_message(filters.command("userlist", "") & filters.me)
async def userlist(client, msg: Message):
    data = DATA["list"]["user"]
    if data == []:
        await msg.edit("لیست خالی است!")
        return
    lists = " لیست یوزر ها : \n\n"
    n = 0
    for i in data:
        n += 1
        lists += f"{n}) `{i}`\n"
    await msg.edit(lists)

@cli.on_message(filters.command("userclean", "") & filters.me)
async def userclean(client, msg: Message):
    DATA["list"]["user"] = []
    save()
    await msg.edit("لیست یوزر ها پاکسازی شد!")


@cli.on_message(filters.command("sendfile", "") & filters.me)
async def send_file(client, msg: Message):
    user = " ".join(msg.command[1:])
    if user:
        lists = ""
        num = 0
        if not int(user) in list_user:
            num += 1
            for i in list_user:
                lists += f"{num}) `{i}`\n"
            await msg.edit(f"چنین ایدی داخل لیست وجود ندارد! \n\n لیست ایدی های موجود : \n{lists}")
            return
        await msg.reply_document(f"txt/text_{user}.txt")
    else:
        for i in list_user:
            await msg.reply_document(f"txt/text_{i}.txt")

@cli.on_message(filters.command("cleanfile", "") & filters.me)
async def clean_file(client, msg: Message):
    user = " ".join(msg.command[1:])
    if user:
        lists = ""
        num = 0
        if not int(user) in list_user:
            num += 1
            for i in list_user:
                lists += f"{num}) `{i}`\n"
            await msg.edit(f"چنین ایدی داخل لیست وجود ندارد! \n\n لیست ایدی های موجود : \n{lists}")
            return
        await msg.reply_text(f"فایل مورد نظر پاک شد!", quote=True)
        os.remove(f"txt/text_{user}.txt")
    else:
        for i in list_user:
            await msg.reply_document(f"txt/text_{i}.txt")
            os.remove(f"txt/text_{i}.txt")
        await msg.edit(f"تمام فایل ها پاکسازی شدند!")


@cli.on_message(filters.text & filters.user(list_user) & ~filters.channel)
async def save_msg(client, msg: Message):
    data = jdatetime.datetime.now().strftime("%y/%m/%d")
    time = datetime.now(pytz.timezone('Asia/Tehran')).strftime('%H:%M:%S')
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    name = msg.from_user.first_name
    msg_id = msg.message_id
    text = msg.text
    msg_text = f"""
--------------------------------------
 USER ID : {user_id}
 CHAT ID : {chat_id}
 FIRST NAME : {name}
 MSG ID : {msg_id}
 TIME : {time}
 DATA : {data}
 TEXT : {text}
--------------------------------------
"""
    print(colored(msg_text, choice(list_color)))
    if int(user_id) in list_user:
        name_file = f"txt/text_{int(user_id)}.txt"
        if not os.path.exists(name_file):
            open(name_file, 'w')
        f = open(name_file, 'r')
        temp = f.read()
        f.close()
        f = open(name_file, 'w')
        f.write(msg_text)
        f.write(temp)
        f.close()



if __name__ == "__main__":
    cli.run()