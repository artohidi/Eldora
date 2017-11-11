import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.replykeyboardremove import ReplyKeyboardRemove

check_answer_number = 0
number = 0
phone_number_set = 0
updater = Updater('491479682:AAH98RAx4c6zGbzXMZBgtcAETKcTsqMz0Sc')
answerKeyboard = [['گزینه د', 'گزینه ج', 'گزینه ب', 'گزینه الف'], ['بازگشت']]
startKeyboard = [['شروع']]
homeKeyboard = [
    ['شرکت در مسابقه'], ['درباره ما'], ['کاتالوگ فنی', 'ليست محصولات'], ['آشنايی با محصولات جديد'],
    ['آشنايي با کارت اصالت و هدايا']]
q_1 = '۱. کدام يک از قطعات زير در سرسيلندر کامل پژو ۱۸۰۰ الدورا مورد استفاده قرار نمی‌گيرد؟\nالف-دوش روغن\nب-خار سوپاپ\nج-کاسه نمد ميل سوپاپ\nد-استکان تايپيت'
q_2 = '۲.کدام يک از قطعات زير در سبد کالای الدورا عرضه می‌گردد؟‌\nالف-ديسک و صفحه\nب-واير شمع\nج-پلوس‌جات\nد-سيم کلاچ'
q_3 = '۳.کدام يک از قطعات زير در سبد کالای الدورا جديد می‌باشد؟\nالف-سوپاپ\nب-شمع موتور\nج-رينگ موتور\nد-بوش و پيستون'
q_4 = '۴.کدام يک از گزينه‌های زير باعث کج شدن سوپاپ می‌شود؟\nالف-سرسيلندر\nب-پاره شدن تسمه تايم\nج-گيرکردن پيستون\nد-سوختن ياتاقان'
q_5 = '۵.کدام يک از گزينه‌های زير از علآل جوش‌آوردن موتور خودرو می‌باشند؟\nالف-ترموستات، رادياتور، سرسيلندر، واشر سرسيلندر\nب-ترموستات، رادياتور، واتر پمپ، کابل منفي باطري\nج-ترموستات، واتر پمپ، واشر سرسيلندر، هوا گرفتن موتور\nد-سرسيلندر، واشر سرسيلندر، واتر پمپ، هوا گرفتن موتور'

aboutUs = "به ربات رسمی الدورا، ارائه‌کننده قطعات یدکی خودرو خوش‌آمدید.\nکانال تلگرامی ما :@ELDORAparts\nآدرس وب سایت:http://www.eldoragroup.com\nتلفن سراسری:۵۲۸۴۳-۰۲۱\nجهت آشنایی با خدمات الدورا و شرکت در مسابقه، کلید شروع در پایین صفحه را لمس نمایید."


def check_answer():
    pass


def user_information(update, phone_number):
    user_id_get = update['message']['chat']['id']
    username_get = update['message']['chat']['username']
    first_name_get = update['message']['chat']['first_name']
    last_name_get = update['message']['chat']['last_name']
    requests.post('http://127.0.0.1:8000/setUserID/', json={"user_id": user_id_get, "username": username_get,
                                                            "first_name": first_name_get, "last_name": last_name_get,
                                                            "phone_number": phone_number})


def set_user_rate(update):
    global check_answer_number
    user_id_get = update['message']['chat']['id']
    requests.post('http://127.0.0.1:8000/setUserRate/', json={"user_id": user_id_get, "rate": check_answer_number})


def get_check_start(user_id):
    data = requests.post('http://127.0.0.1:8000/checkStart/', json={"user_id": user_id})
    return data


def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id, aboutUs, reply_markup=ReplyKeyboardMarkup(homeKeyboard))


def message_handler(bot, update):
    global number, phone_number_set, check_answer_number
    message = update.message.text
    chat_id = update.message.chat_id
    if phone_number_set == 1:
        phone_number = update.message.text
        user_information(update, phone_number)
        phone_number_set = 0
        bot.send_message(chat_id,
                         "شماره تماس شما با موفقیت در سیستم ثبت گردید، لطفاً برای شروع مسابقه دکمه شروع را لمس نمایید:",
                         reply_markup=ReplyKeyboardMarkup(startKeyboard))
    else:
        if message == "شروع":
            bot.send_message(chat_id, "لطفاً به سوالات زیر پاسخ دهید:")
            bot.send_message(chat_id, q_1, reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
            number = 1
        elif message == "شرکت در مسابقه":
            first_start = get_check_start(chat_id).json()['start']
            if first_start == "شروع نکرده":
                if phone_number_set == 0:
                    bot.send_message(chat_id, "لطفاً شماره تماس خود را جهت شرکت در مسابقه وارد نمایید:",
                                     reply_markup=ReplyKeyboardRemove())
                    phone_number_set = 1
            elif first_start == "شروع کرده":
                bot.send_message(chat_id, "شما قبلاً در مسابقه شرکت کرده‌اید.",
                                 reply_markup=ReplyKeyboardMarkup(homeKeyboard))
        elif message == 'گزینه الف' or message == 'گزینه ب' or message == 'گزینه ج' or message == 'گزینه د':
            if number < 6:
                if number == 1:
                    number = 2
                    if message == 'گزینه الف':
                        check_answer_number = check_answer_number + 1
                    bot.send_message(chat_id, q_2,
                                     reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
                elif number == 2:
                    number = 3
                    if message == 'گزینه ج':
                        check_answer_number = check_answer_number + 1
                    bot.send_message(chat_id, q_3,
                                     reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
                elif number == 3:
                    number = 4
                    if message == 'گزینه ب':
                        check_answer_number = check_answer_number + 1
                    bot.send_message(chat_id, q_4,
                                     reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
                elif number == 4:
                    number = 5
                    if message == 'گزینه ب':
                        check_answer_number = check_answer_number + 1
                    bot.send_message(chat_id, q_5,
                                     reply_markup=ReplyKeyboardMarkup(answerKeyboard, resize_keyboard=True))
                elif number == 5:
                    if message == 'گزینه ب':
                        check_answer_number = check_answer_number + 1
                    set_user_rate(update)
                    if check_answer_number > 3:
                        bot.send_message(chat_id,
                                         "شرکت کننده گرامی، شما به حداقل ۴ سوال پاسخ صحیح داده‌اید و شماره شما جهت شرکت در قرعه‌کشی ثبت گردید. نتایج قرعه‌کشی در تاریخ دوشنبه مورخ ۱۳۹۶/۸/۹ در کانال تلگرام @ELDORAparts اطلاع‌رسانی خواهد‌شد.",
                                         reply_markup=ReplyKeyboardMarkup(homeKeyboard))
                    elif check_answer_number < 3:
                        bot.send_message(chat_id, "از اینکه در مسابقه شرکت کرده‌اید، بسیار سپاسگزاریم.",
                                         reply_markup=ReplyKeyboardMarkup(homeKeyboard))

        elif message == "درباره ما":
            bot.send_message(chat_id,
                             "الدورا با آغاز فعالیت از سال ۱۳۸۷:\n 🔹 با عرضه قطعات یدکی خودرو با کیفیت عالی\n 🔹 با ارائه خدمات پس از فروش در سطح معیارهای جهانی\n 🔹 با شبکه گسترده توزیع در سطح کشور\n 🔹 و با عزمی راسخ در پی تحقق رشد و توسعه همه جانبه و پایدار توانسته است سطح استاندارد  کیفی این بازار را ارتقاء داده و رضایت و خشنودی مشتریان را برآورده نماید.")

        elif message == "کاتالوگ فنی":
            bot.forward_message(chat_id=chat_id, from_chat_id=79733373, message_id=18)
        elif message == "ليست محصولات":
            bot.forward_message(chat_id=chat_id, from_chat_id=79733373, message_id=185)
        elif message == "آشنايی با محصولات جديد":
            bot.forward_message(chat_id=chat_id, from_chat_id=79733373, message_id=185)
        elif message == "آشنايي با کارت اصالت و هدايا":
            bot.send_message(chat_id,
                             "شما می‌توانید از طریق ارائه رمز کارت اصالت به سامانه پیامکی، علاوه بر حصول اطمینان از اصالت کالا و استفاده از خدمات پس از فروش، امتیاز جمع‌آوری کرده و ضمن دریافت جوایز نقدی در قرعه‌کشی‌های فصلی و سالانه ما شرکت نمایید. جهت کسب اطلاعات بیشتر عدد ۹ را به سامانه ۳۰۰۰۷۷۰۱ ارسال نمایید.")
        else:
            bot.send_message(chat_id, 'عبارت وارد‌شده صحیح نمی‌باشد.', reply_markup=ReplyKeyboardMarkup(homeKeyboard))


if __name__ == '__main__':
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler([Filters.text], message_handler))
    updater.start_polling()
