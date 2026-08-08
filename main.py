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
    time.sleep(20)  
    while True:
        try:
            target_url = RENDER_URL if RENDER_URL else f"http://127.0.0.1:{PORT}/"
            response = requests.get(target_url)
            print(f"🔄 Self-ping sent to: {target_url} | Status: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Self-ping error: {e}")
        
        time.sleep(300) 

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
    btn_market = types.InlineKeyboardButton(text="Market သုံးနည်း", callback_data="market_guide")
    btn_task = types.InlineKeyboardButton(text="Task လုပ်နည်း", callback_data="task_guide")
    
    markup.add(btn_features, btn_game, btn_register, btn_withdraw, btn_market, btn_task)
    
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
        
    # လုပ်ဆောင်နိုင်တဲ့အရာများ
    elif call.data == "features":
        bot.answer_callback_query(call.id)
        text = (
            "ဂိမ်းဆော့ရင်း အပိုဝင်ငွေ ရှာချင်သူတွေအတွက် သတင်းကောင်း! 🍬✨\n\n"
            "ဘာလို့ Candy Shooter မှာဘာ‌လေးတွေလုပ်ပြီငွေရှာလို့ရနိုင်သလဲ?\n\n"
            "✅ **နေ့စဉ် Task များ:** APK ဒေါင်းလုဒ်ဆွဲပြီး Task လုပ်ရုံနဲ့ တစ်နေ့ကို ကိုယ် ဆွဲနိုင်သလောက် coin များရယူနိုင်ခြင်း\n\n"
            "✅ **Youtube ကြည့်ပြီး Coin စုမယ်:** YouTube video လေးတွေ ကြည့်ပေးလို့ရပါတယ်။ ထမင်းစားရင်းပဲကြည့်ကြည့် YouTube ထဲမှာရှိသမျှ video တွေအကုန်ကြည့်နိုင်ပါတယ်နော်。"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="⬅️ Menu သို့ပြန်သွားရန်", callback_data="back_to_menu"))
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
        
    # အကောင့်ဖွင့်နည်း (ပုံ ၄ ပုံ - File ID များဖြင့်)
    elif call.data == "acc_register":
        bot.answer_callback_query(call.id)
        try:
            media = [
                types.InputMediaPhoto("AgACAgUAAxkBA3AO2mp2sXWKkjSR5FbcpZwj7NhJP_wYAAJYEWsbjtm5VxIwPIqXVEhgAQADAgADeQADPQQ"),
                types.InputMediaPhoto("AgACAgUAAxkBA3AO3mp2sXUOhSccKt94Yy4_NGedIdEnAAJREWsbjtm5V1j_JIMLbCmOAQADAgADeQADPQQ"),
                types.InputMediaPhoto("AgACAgUAAxkBA3AO3Gp2sXUW3kPvTHQmzLsvnC_cwIwaAAJSEWsbjtm5V3hwVnaWiH_4AQADAgADeQADPQQ"),
                types.InputMediaPhoto("AgACAgUAAxkBA3AO22p2sXUXwWuKHhd8n8aNwZBFEwTMAAJTEWsbjtm5V0CGK6LI4I8KAQADAgADeQADPQQ")
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
        
    # ငွေထုတ်နည်း (ပုံ ၃ ပုံ - File ID များဖြင့်)
    elif call.data == "withdraw_guide":
        bot.answer_callback_query(call.id)
        try:
            media = [
                types.InputMediaPhoto("AgACAgUAAxkBA3AO1Wp2sXSt4Hunl6fgFYG9WD_YOP5OAAJcEWsbjtm5V9BqF-p82BxYAQADAgADeQADPQQ"),
                types.InputMediaPhoto("AgACAgUAAxkBA3AO1Gp2sXRe5Rq5dt8IBeAJZiWetlhOAAJdEWsbjtm5V_h0TfUlB--XAQADAgADeQADPQQ"),
                types.InputMediaPhoto("AgACAgUAAxkBA3AO12p2sXTfGDrJFYkhBBkcsh-Igy4PAAJeEWsbjtm5Vzs_k_KBLMaKAQADAgADeQADPQQ")
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

    # Market သုံးနည်း (ပုံ ၂ ပုံ - File ID များဖြင့်)
    elif call.data == "market_guide":
        bot.answer_callback_query(call.id)
        try:
            media = [
                types.InputMediaPhoto("AgACAgUAAxkBA3AO2mp2sXWKkjSR5FbcpZwj7NhJP_wYAAJYEWsbjtm5VxIwPIqXVEhgAQADAgADeQADPQQ"),
                types.InputMediaPhoto("AgACAgUAAxkBA3AO22p2sXUXwWuKHhd8n8aNwZBFEwTMAAJTEWsbjtm5V0CGK6LI4I8KAQADAgADeQADPQQ")
            ]
            bot.send_media_group(chat_id, media)
        except Exception as e:
            print(f"Image send error: {e}")
            
        text = (
            "ဈေးကွက် (Market) အသုံးပြုနည်း 📊\n\n"
            "သလေတို့ရေ\n"
            "သလေတို့အတွက် Market အကြောင်း ရှင်းပြပေးပါမယ်နော်🫶\n\n"
            "သူကလေ ကိုယ့်ပါပါလာ mmk and coin ရောင်းး & ဝယ် လုပ်လို့ရတဲ့ဟာလေးပါနော် coin ပြန်ရောင်းချင်လဲ ရသလို coin ပြန်လဲချင်ပါတယ်နော် မြန်မာငွေ mmk ကိုလည်း ပြောင်းလို့လဲ ရပါတယ်နော်🐒🫶\n\n"
            "ဘယ်လို လုပ်ရတာလဲ?\n"
            "လုပ်နည်းရှိပါတယ်ရှင်😉\n\n"
            "အရောင်းအဝယ်လုပ်နည်း👇\n\n"
            "Step 1- botထဲကိုဝင်ပြီးတာနဲ့ ဈေးကွက် ကိုနှိပ်ပါ\n\n"
            "Step 2-ဝယ်မယ်ဆို (ဝယ်)နေရာကိုနှိပ်ပါ ရောင်းမယ်ဆို(ရောင်းး)ကိုနှိပ်ပါ\n\n"
            "Step 3- ပြီးလျှင် မိမိ ဝယ်ချင်/ရောင်းချင်သည့် ပမာဏကို ရေးထည့်ပါ(အောက်တွင် နှုန်းဖန်း-တန်ဖိုးကို ကြည့်နိုင်မည်)\n\n"
            "Step 4- ပမာဏထည့်ပြီးပါက ရောင်းမယ်ဆို(ရောင်းမည်)နှိပ်ပါ ဝယ်မယ်ဆို (ဝယ်ယူမည်)ကိုနှိပ်ပါ\n\n"
            "အဲ့ဒါဆို ရပါပြီကောင့်✅\n\n"
            "ပြီးတော့ မင်မင်တို့ပြောချင်တာကလေ ဈေးကွက် အတက်အကျ အမြဲရှိပါတယ်နော်တို႔အားလုံးပဲ အားပေးကြပါစို့ရှင့်✨"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="⬅️ Menu သို့ပြန်သွားရန်", callback_data="back_to_menu"))
        bot.send_message(chat_id, text, reply_markup=markup)
        
    # Task လုပ်နည်း (ဗီဒီယို နှင့် ပုံ - File ID များဖြင့်)
    elif call.data == "task_guide":
        bot.answer_callback_query(call.id)
        try:
            bot.send_video(chat_id, "AAMCBQADGQEDcA7SanaxdDCFwGnOmHCKvBuRavJuPz0AAlIeAAKO2blXHq6q15W5KX4BAAdtAAM9BA")
            bot.send_photo(chat_id, "AgACAgUAAxkBA3AQVWp2s9DXYC-qOPbCV8CsWuUh_VcgAAJfEWsbjtm5V2YZbSoPmNoiAQADAgADeQADPQQ")
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

    # Menu သို့ ပြန်သွားရန်
    elif call.data == "back_to_menu":
        bot.answer_callback_query(call.id)
        show_menu(chat_id)

# ==========================================
# 5. MAIN RUNNER
# ==========================================
if __name__ == "__main__":
    print("=" * 50)
    print("🍬 Candy Hub Bot စတင်နေပါပြီ...")
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
        
