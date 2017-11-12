import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.replykeyboardremove import ReplyKeyboardRemove

updater = Updater('491479682:AAH98RAx4c6zGbzXMZBgtcAETKcTsqMz0Sc')
answerKeyboard = [['گزینه د', 'گزینه ج', 'گزینه ب', 'گزینه الف']]
startKeyboard = [['شروع']]
homeKeyboard = [
    ['شرکت در مسابقه'], ['درباره ما'], ['کاتالوگ فنی', 'ليست محصولات'], ['آشنايی با محصولات جديد'],
    ['آشنايي با کارت اصالت و هدايا']
]
q_1 = '۱. کدام يک از قطعات زير در سرسيلندر کامل پژو ۱۸۰۰ الدورا مورد استفاده قرار نمی‌گيرد؟\nالف-دوش روغن\nب-خار سوپاپ\nج-کاسه نمد ميل سوپاپ\nد-استکان تايپيت'
q_2 = '۲.کدام يک از قطعات زير در سبد کالای الدورا عرضه می‌گردد؟‌\nالف-ديسک و صفحه\nب-واير شمع\nج-پلوس‌جات\nد-سيم کلاچ'
q_3 = '۳.کدام يک از قطعات زير در سبد کالای الدورا جديد می‌باشد؟\nالف-سوپاپ\nب-شمع موتور\nج-رينگ موتور\nد-بوش و پيستون'
q_4 = '۴.کدام يک از گزينه‌های زير باعث کج شدن سوپاپ می‌شود؟\nالف-سرسيلندر\nب-پاره شدن تسمه تايم\nج-گيرکردن پيستون\nد-سوختن ياتاقان'
q_5 = '۵.کدام يک از گزينه‌های زير از علّل جوش‌آوردن موتور خودرو می‌باشند؟\nالف-ترموستات، رادياتور، سرسيلندر، واشر سرسيلندر\nب-ترموستات، رادياتور، واتر پمپ، کابل منفي باطري\nج-ترموستات، واتر پمپ، واشر سرسيلندر، هوا گرفتن موتور\nد-سرسيلندر، واشر سرسيلندر، واتر پمپ، هوا گرفتن موتور'


def set_user_id(update, user_state):  # good
    user_id_get = update.message.chat_id
    username_get = update.message.chat.username
    first_name_get = update.message.chat.first_name
    last_name_get = update.message.chat.last_name
    user_rate_get = "0"
    requests.post('http://127.0.0.1:8000/setUserId/', json={"user_id": user_id_get, "username": username_get,
                                                            "first_name": first_name_get, "last_name": last_name_get,
                                                            "rate": user_rate_get, "state": user_state})


def set_user_phone_number(chat_id, phone_number):  # good
    requests.post('http://127.0.0.1:8000/setPhoneNumber/', json={"user_id": chat_id, "phone_number": phone_number})


def set_user_state(chat_id, user_state):
    requests.post('http://127.0.0.1:8000/setUserState/', json={"user_id": chat_id, "state": user_state})


def set_user_start(chat_id, user_start):
    requests.post('http://127.0.0.1:8000/setUserStart/', json={"user_id": chat_id, "start": user_start})


def set_user_phone_state(chat_id, phone_state):
    requests.post('http://127.0.0.1:8000/setPhoneState/', json={"user_id": chat_id, "phone_state": phone_state})


def set_user_rate(chat_id, user_rate):
    requests.post('http://127.0.0.1:8000/setUserRate/', json={"user_id": chat_id, "rate": user_rate})


def get_user(user_id):
    data = requests.post('http://127.0.0.1:8000/getUser/', json={"user_id": user_id})
    return data


def start(bot, update):
    chat_id = update.message.chat_id
    set_user_id(update, "شروع")
    bot.send_message(chat_id, "لطفاً انتخاب نمایید:", reply_markup=ReplyKeyboardMarkup(homeKeyboard))


def message_handler(bot, update):
    message = update.message.text
    chat_id = update.message.chat_id
    user_data = get_user(chat_id).json()
    user_state = user_data["user_state"]
    user_rate = user_data["user_rate"]
    phone_number_state = user_data["phone_state"]
    user_start = user_data["start"]
    if phone_number_state == "1":
        set_user_start(chat_id, "شروع کرده")
        set_user_state(chat_id, "دریافت شماره تماس")
        set_user_phone_number(chat_id, message)
        set_user_phone_state(chat_id, "0")
        bot.send_message(chat_id,
                         "شماره تماس شما با موفقیت در سیستم ثبت گردید، لطفاً برای شروع مسابقه دکمه شروع را لمس نمایید:",
                         reply_markup=ReplyKeyboardMarkup(startKeyboard))
    else:
        if message == "شروع":
            set_user_state(chat_id, "سوال اول")
            bot.send_message(chat_id, "لطفاً به سوالات زیر پاسخ دهید:")
            bot.send_message(chat_id, q_1, reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
        elif message == "شرکت در مسابقه":
            if user_start == "شروع نکرده":
                set_user_state(chat_id, "ثبت موبایل")
                bot.send_message(chat_id, "لطفاً شماره تماس خود را جهت شرکت در مسابقه وارد نمایید:",
                                 reply_markup=ReplyKeyboardRemove())
                set_user_phone_state(chat_id, "1")
            elif user_start == "شروع کرده":
                bot.send_message(chat_id,
                                 "شرکت کننده گرامی، شماره شما در سیستم ثبت شده‌است. لطفا مجدداً تلاش نفرمایید.",
                                 reply_markup=ReplyKeyboardMarkup(homeKeyboard))
        elif message == 'گزینه الف' or message == 'گزینه ب' or message == 'گزینه ج' or message == 'گزینه د':
            if user_state == "سوال اول":
                set_user_state(chat_id, "سوال دوم")
                if message == 'گزینه الف':
                    set_user_rate(chat_id, str(int(user_rate) + 1))
                bot.send_message(chat_id, q_2,
                                 reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
            elif user_state == "سوال دوم":
                set_user_state(chat_id, "سوال سوم")
                if message == 'گزینه ج':
                    set_user_rate(chat_id, str(int(user_rate) + 1))
                bot.send_message(chat_id, q_3,
                                 reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
            elif user_state == "سوال سوم":
                set_user_state(chat_id, "سوال چهارم")
                if message == 'گزینه ب':
                    set_user_rate(chat_id, str(int(user_rate) + 1))
                bot.send_message(chat_id, q_4,
                                 reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
            elif user_state == "سوال چهارم":
                set_user_state(chat_id, "سوال پنجم")
                if message == 'گزینه ب':
                    set_user_rate(chat_id, str(int(user_rate) + 1))
                bot.send_message(chat_id, q_5,
                                 reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
            elif user_state == "سوال پنجم":
                if message == 'گزینه ب':
                    set_user_rate(chat_id, str(int(user_rate) + 1))
                set_user_state(chat_id, "پایان مسابقه")
                if int(user_rate) > 3:
                    bot.send_message(chat_id,
                                     "شرکت کننده گرامی، شما به حداقل ۴ سوال پاسخ صحیح داده‌اید و شماره شما جهت شرکت در قرعه‌کشی ثبت گردید. نتایج قرعه‌کشی در تاریخ دوشنبه مورخ ۱۳۹۶/۸/۹ در کانال تلگرام @ELDORAparts اطلاع‌رسانی خواهد‌شد.",
                                     reply_markup=ReplyKeyboardMarkup(homeKeyboard))
                elif int(user_rate) < 3:
                    bot.send_message(chat_id,
                                     "شرکت کننده گرامی، با سپاس از مشارکت شما. متاسفانه تعداد پاسخ‌های درست شما جهت شرکت در قرعه‌کشی کمتر از ۴ می‌باشد. لطفا جهت آشنایی بیشتر با ما درباره ما را کلید کنید.",
                                     reply_markup=ReplyKeyboardMarkup(homeKeyboard))

        elif message == "درباره ما":
            set_user_state(chat_id, "درباره ما")
            bot.send_message(chat_id,
                             "الدورا با آغاز فعالیت از سال ۱۳۸۷:\n 🔹 با عرضه قطعات یدکی خودرو با کیفیت عالی\n 🔹 با ارائه خدمات پس از فروش در سطح معیارهای جهانی\n 🔹 با شبکه گسترده توزیع در سطح کشور\n 🔹 و با عزمی راسخ در پی تحقق رشد و توسعه همه جانبه و پایدار توانسته است سطح استاندارد  کیفی این بازار را ارتقاء داده و رضایت و خشنودی مشتریان را برآورده نماید.")

        elif message == "کاتالوگ فنی":
            set_user_state(chat_id, "کاتالوگ فنی")
            bot.forward_message(chat_id=chat_id, from_chat_id=79733373, message_id=18)
        elif message == "ليست محصولات":
            set_user_state(chat_id, "لیست محصولات")
            bot.forward_message(chat_id=chat_id, from_chat_id=79733373, message_id=185)
        elif message == "آشنايی با محصولات جديد":
            set_user_state(chat_id, "آشنایی با محصولات جدید")
            bot.forward_message(chat_id=chat_id, from_chat_id=79733373, message_id=185)
        elif message == "آشنايي با کارت اصالت و هدايا":
            set_user_state(chat_id, "آشنایی با کارت اصالت و هدایا")
            bot.send_message(chat_id,
                             "شما می‌توانید از طریق ارائه رمز کارت اصالت به سامانه پیامکی، علاوه بر حصول اطمینان از اصالت کالا و استفاده از خدمات پس از فروش، امتیاز جمع‌آوری کرده و ضمن دریافت جوایز نقدی در قرعه‌کشی‌های فصلی و سالانه ما شرکت نمایید. جهت کسب اطلاعات بیشتر عدد ۹ را به سامانه ۳۰۰۰۷۷۰۱ ارسال نمایید.")
        else:
            bot.send_message(chat_id, 'عبارت وارد‌شده صحیح نمی‌باشد.', reply_markup=ReplyKeyboardMarkup(homeKeyboard))


if __name__ == '__main__':
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler([Filters.text], message_handler))
    updater.start_polling()
