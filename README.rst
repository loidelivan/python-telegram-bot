pip install python-telegram-bot --upgrade
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Reemplaza 'YOUR_TOKEN_HERE' con el token que te dio BotFather
TOKEN = '7638517033:AAEG-4IXKTUorrVJZN8ymW5F923pqrnezhI'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy un bot simple de Telegram.')

def main():
    # Crea el updater y el dispatcher
    updater = Updater(TOKEN)

    # Obtén el dispatcher para registrar los manejadores
    dispatcher = updater.dispatcher

    # Registra el manejador de comandos
    dispatcher.add_handler(CommandHandler('start', start))

    # Inicia el bot
    updater.start_polling()

    # Ejecuta el bot hasta que se detenga
    updater.idle()

if __name__ == '__main__':
    main()
