from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import importlib
import deck_scraper as ds
print("Бот запущен. Нажмите Ctrl+C для завершения")

token = "5052117026:AAFh_KnSF4Zkz0zJIW_vIua2u9veN0qM-Y8"

def on_start(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Привет, я Вiтковський")
def on_message(update, context):
    chat = update.effective_chat
    text = update.message.text
    try:
        importlib.reload(ds)
        context.bot.send_message(chat_id=chat.id, text=ds.get_golden(text))
    except:
        context.bot.send_message(chat_id=chat.id, text='Wrong URL! Send a deck link!')
updater = Updater(token, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(MessageHandler(Filters.all, on_message))

updater.start_polling()
updater.idle()


