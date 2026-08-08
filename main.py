import os
import time
import requests
import threading
from flask import Flask
import telebot
from telebot import types

# ==========================================
# 1. CONFIGURATION
# ==========================================
BOT_TOKEN = "8946305512:AAEf9obGZhn9iix6CoUa0jMwRa1ngfWDmNU"
ADMIN_GROUP_ID = "-100123456789"  # မိမိရဲ့ Admin Group ID

bot = telebot.TeleBot(BOT_TOKEN)

# Render Dynamic Port ကို ယူခြင်း (Default = 8080)
PORT = int(os.environ.get("PORT", 8080))

# Render က ပေးမည့် Public URL ကို Auto ယူခြင်း
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "")

# ==========================================
# 2. FLASK SERVER & SELF-PING SYSTEM
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Candy Hub Bot is Alive & Running on Render Web Service!"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

def ping_self():
    """ 
    Render Web Service မအိပ်သွားစေရန် ၅ မိနစ်တစ်ကြိမ် 
    မိမိ Public URL သို့ ping ပို့ပေးသည့် စနစ်
    """
    time.sleep(20)  # Server စတင်တက်လာအောင် ၂၀ စက္ကန့် စောင့်မည်
    while True:
        try:
            target_url = RENDER_URL if RENDER_URL else f"http://127.0.0.1:{PORT}/"
            response = requests.get(target_url)
            print(f"🔄 Self-ping sent to: {target_url} | Status: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Self-ping error: {e}")
        
        time.sleep(300)  # ၅ မိနစ် (၃၀၀ စက္ကန့်) ခြားတစ်ကြိမ် ping ပါမည်

# ==========================================
# 3. BOT COMMAND HANDLERS
# ==========================================

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    start_text = (
        f"Hi {user_name} 🐻\n\n"
        "I am candy hub assistant\n\n"
        "Join system\n\n"
        "အောက်ပါလင့်လေးတွေ join ပေးပါနော်\n\n"
        "─────────────────\n"
        "Check system\n\n"
        "Gp & channel များကို join ပြီးပါက စစ်ရန်\n"
        "👇"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_channel = types.InlineKeyboardButton(text="channel", url="https://t.me/CandyHub_Ch")
    btn_chat = types.InlineKeyboardButton(text="Chat", url="https://t.me/CandyHub_Chat")
    btn_check = types.InlineKeyboardButton(text="Check", callback_data="check_join")
    
    markup.add(btn_channel, btn_chat)
    markup.add(btn_check)
    
    bot.reply_to(message, start_text, reply_markup=markup)

# /menu command
@bot.message_handler(commands=['menu'])
def send_menu(message):
    show_menu(message.chat.id)

# Menu ခလုတ်များ ပြသပေးသည့် Function
def show_menu(chat_id):
    menu_text = "🍬 **Candy Hub Menu**\n\nအောက်ပါ ခလုတ်များမှ မိမိကြည့်ရှုလိုသည်ကို နှိပ်ပါနော်:"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_features = types.InlineKeyboardButton(text="လုပ်ဆောင်နိုင်တဲ့အရာများ", callback_data="features")
    btn_game = types.InlineKeyboardButton(text="ဂိမ်းလင့်", url="https://t.me/CandyHub8_bot/app?startapp=jpBACimToMNYu3xnnvCSLoz6vqi2")
    btn_register = types.InlineKeyboardButton(text="အကောင့်ဖွင့်နည်း", callback_data="acc_register")
    btn_withdraw = types.InlineKeyboardButton(text="ငွေထုတ်နည်း", callback_data="withdraw_guide")
    btn_task = types.InlineKeyboardButton(text="task လုပ်နည်း", callback_data="task_guide")
    
    markup.add(btn_features, btn_game, btn_register, btn_withdraw, btn_task)
    
    bot.send_message(chat_id, menu_text, reply_markup=markup, parse_mode="Markdown")

# ==========================================
# 4. CALLBACK BUTTONS HANDLER
# ==========================================
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    
    # Check Button
    if call.data == "check_join":
        bot.answer_callback_query(call.id, text="စစ်ဆေးမှု အောင်မြင်ပါသည်။")
        show_menu(chat_id)
        
    # Button 1: လုပ်ဆောင်နိုင်တဲ့အရာများ
    elif call.data == "features":
        bot.answer_callback_query(call.id)
        text = (
            "ဂိမ်းဆော့ရင်း အပိုဝင်ငွေ ရှာချင်သူတွေအတွက် သတင်းကောင်း! 🍬✨\n\n"
            "ဘာလို့ Candy Shooter မှာဘာ‌လေးတွေလုပ်ပြီငွေရှာလို့ရနိုင်သလဲ?\n\n"
            "✅ **နေ့စဉ် Task များ:** APK ဒေါင်းလုဒ်ဆွဲပြီး Task လုပ်ရုံနဲ့ တစ်နေ့ကို ကိုယ် ဆွဲနိုင်သလောက် coin များရယူနိုင်ခြင်း\n\n"
            "✅ **Youtube ကြည့်ပြီး Coin စုမယ်:** YouTube video လေးတွေ ကြည့်ပေးလို့ရပါတယ်။ ထမင်းစားရင်းပဲကြည့်ကြည့် YouTube ထဲမှာရှိသမျှ video တွေအကုန်ကြည့်နိုင်ပါတယ်နော်။"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="⬅️ Menu သို့ပြန်သွားရန်", callback_data="back_to_menu"))
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
        
    # Button 3: အကောင့်ဖွင့်နည်း
    elif call.data == "acc_register":
        bot.answer_callback_query(call.id)
        try:
            media = [
                types.InputMediaPhoto(open('acc_1.jpg', 'rb')),
                types.InputMediaPhoto(open('acc_2.jpg', 'rb')),
                types.InputMediaPhoto(open('acc_3.jpg', 'rb')),
                types.InputMediaPhoto(open('acc_4.jpg', 'rb'))
            ]
            bot.send_media_group(chat_id, media)
        except Exception as e:
            print(f"Image send error: {e}")
            
        text = (
            "Acc ဖွင့်နည်း💳\n\n"
            "1. t.me/CandyHub8_bot/app?startapp=jpBACimToMNYu3xnnvCSLoz6vqi2  ဒီbot လေးကိုနှိပ်ပေးပါ။📱\n\n"
            "2. ၀င်ပြိးပါက profile လူအဖြူပုံလေးနှိပ်ပါ။🖱\n\n"
            "3. အကောင့်ဖွင့်ရန်ဆိုတဲ့ ခလုတ်လေးနှိပ်ပါ။📱\n\n"
            "4. အကောင့်ဖွင့်ရန်ဆိုတဲ့ဘက်ကိုနှိပ်ပါ။📱\n\n"
            "5. နေရာ 4 ခုရှိပါမယ် မထမနေရာမှာ မိမိ၏ အမည် သို့မဟုတ် ကြိုက်တဲ့ နာမည်ထည့်ပါ။\n"
            "အီးမေစလ် နေရာမှာ မိမိ၏ Gmail ထည့်ပေးပါ။\n"
            "စကားဝှက်မှာ မိမိ ထားချင်တဲ့ နံပါတ်ထည့်ပါ။\n"
            "အောက်တကွက်မှာစောနက ထည့်ထားတဲ့ စကားဝှက်ထက်ထည့်ပါ။📱\n\n"
            "6. ထိုအခါ အကောင့် ဖွင့်ခြင်းပြီးဆုံးပါပီ့။🥳\n\n"
            "⚠️❌ သတိ မိမိရဲ့ email နဲ့ password ကို ss screenshot ရိုက်‌ထားပါ။📲"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="⬅️ Menu သို့ပြန်သွားရန်", callback_data="back_to_menu"))
        bot.send_message(chat_id, text, reply_markup=markup, disable_web_page_preview=True)
        
    # Button 5: ငွေထုတ်နည်း
    elif call.data == "withdraw_guide":
        bot.answer_callback_query(call.id)
        try:
            media = [
                types.InputMediaPhoto(open('withdraw_1.jpg', 'rb')),
                types.InputMediaPhoto(open('withdraw_2.jpg', 'rb')),
                types.InputMediaPhoto(open('withdraw_3.jpg', 'rb'))
            ]
            bot.send_media_group(chat_id, media)
        except Exception as e:
            print(f"Image send error: {e}")
            
        text = (
            "ငွေထုတ်နည်း💸\n\n"
            "1. ငွေထုတ်ဆိုတဲ့ ပိုက်ဆံအိတ်ကိုသွားပါ။\n\n"
            "2. ကိုယ်ထုတ်မဲ့ payment ကိုရွေးချယ်ပါ။🪪\n\n"
            "3. မိမိထုတ်မည့်ပမာဏကိုထည့်ပါ။💸\n"
            "ထုတ်မည့် ပမာဏသည် ကိုယ့် မြန်မာငွေရဲ့ တစ်၀က်ကိုသာထုတ်ခွင့်ပေးပါသည်။📍\n"
            "ပမာဏသည် စုံကိန်းဖြစ်ရပါမည်။💶\n\n"
            "4. အကောင့်ပိုရှင်နေရာ မှာ wave သို့မဟုတ် kpay ရဲ့ အကောင့် name ကို ထည့်ပေးပါ။💳\n\n"
            "5. ဖုန်းနံပါတ်မှာ kpay သို့မဟုတ် wave ရဲ့ ဖုန်းနံပါတ်ထည့်ပေးပါ။💳\n\n"
            "ဖုန်းနံပါတ် မှားသွားပါက မေတ္တာဖြင့် ငွေပြန်လွှဲ‌ပေးနိုင်မည်မဟုတ်ပါ။❌❌\n\n"
            "အားလုံးပဲကျေးဇူးတင်ပါတယ်ရှင့်။😚"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="⬅️ Menu သို့ပြန်သွားရန်", callback_data="back_to_menu"))
        bot.send_message(chat_id, text, reply_markup=markup)
        
    # Button 6: Task လုပ်နည်း
    elif call.data == "task_guide":
        bot.answer_callback_query(call.id)
        try:
            bot.send_video(chat_id, open('task_video.mp4', 'rb'))
            bot.send_photo(chat_id, open('task_sample.jpg', 'rb'))
        except Exception as e:
            print(f"Media send error: {e}")
            
        text = (
            "{Task} လုပ်နည်း video ပါ video လုပ်ထားတာလေးကတော့နဲ့နဲ့ညံ့တော့သီးခံကြည့်ပေးကြပါ😅\n\n"
            "{Task} တင်ရမဲ့နမူနာပုံပါပါတယ်သေခြာကြည့်ပေးကြပါ❗️\n\n"
            "{Task} တင်တဲ့အခါဒီနေ့တင်တဲ့ဟာဆိုနောက်နေ့မနက် ၇နာရီ၈နာရီကျော်ကြားမှာစစ်ပေးပါတယ်✅\n\n"
            "{Task} တင်တဲ့အခါမတူညီတဲ့ app 2ခုကိုအတက်နိုင်‌ဆုံး download တင်ပေးကြပါခင်ဗျာတင်ပြီးသားကြီးထက်တင်တာမျိုးတွေပြန်မတင်ကြပါနဲ့နော်💸\n\n"
            "{Task} ကို bot မှာတင်မရတာမျိုး‌အခက်အခဲတစ်ခုကြောင့် bot ထဲမဝင်ဖြစ်လို့ coins mmk တွေနှုတ်ခံရတာမျိုးဖြစ်ရင် @arkar2455 ကိုလာပြောပေးကြပါ👀\n\n"
            "{Task} တင်တဲ့အခါ app download ထားတာတွေကိုရက်ဆက်ကြီး ပုံတူတွေတင်မိတာ app ဆင်တူတွေတင်မိတာမျိုးဆိုbanခံရနိုင်ပါတယ် app download တာတစ်ခုကတော့မတူအောင် download ပေးကြပါ တစ်ချို့လူတွေ app တစ်ခုထဲ download တာတွေရှိပါတယ်နှစ်ခု‌ download ပေးကြပါ⚠️"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="⬅️ Menu သို့ပြန်သွားရန်", callback_data="back_to_menu"))
        bot.send_message(chat_id, text, reply_markup=markup)

    # Back to Menu Button
    elif call.data == "back_to_menu":
        bot.answer_callback_query(call.id)
        show_menu(chat_id)

# ==========================================
# 5. MAIN RUNNER
# ==========================================
if __name__ == "__main__":
    print("=" * 50)
    print("🍬 Candy Hub Bot စတင်နေပါပြီ...")
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"🌐 Running on Port: {PORT}")
    print("=" * 50)

    # 1. Flask server ကို Background Thread ဖြင့် Run သည့်စနစ်
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print("✅ Flask Web Server started successfully")

    # 2. Self-ping ကို Background Thread ဖြင့် Run သည့်စနစ်
    ping_thread = threading.Thread(target=ping_self)
    ping_thread.daemon = True
    ping_thread.start()
    print("✅ Self-ping Background System started successfully")

    # 3. Webhook ဖျက်ပြီး Polling စတင်ခြင်း
    try:
        bot.remove_webhook()
        print("✅ Webhook removed successfully")
    except Exception as e:
        print(f"⚠️ Webhook removal error: {e}")

    print("=" * 50)
    print("🤖 Bot is now live and waiting for requests...")
    print("=" * 50)

    # Server မရပ်ဘဲ ၅ စက္ကန့်ခြား Auto Reconnect လုပ်ပေးသော Loop
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ Polling error: {e}")
            print("🔄 Reconnecting in 5 seconds...")
            time.sleep(5)
      
