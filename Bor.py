pip install python-telegram-bot
from telegram import Update, ChatMember
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time

# Diccionario para llevar el conteo de advertencias
user_warnings = {}

# Función que responderá al comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy tu bot de Telegram.')

# Función que responderá al comando /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¿Cómo puedo ayudarte?')

# Función para filtrar enlaces
def filter_links(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id

    # Verifica si el usuario es un administrador
    member = context.bot.get_chat_member(chat_id, user_id)

    if member.status not in [ChatMember.ADMINISTRATOR, ChatMember.CREATOR]:
        if 'http://' in update.message.text or 'https://' in update.message.text:
            # Agregar advertencia
            add_warning(update, user_id, context)
            update.message.delete()
            update.message.reply_text('No puedes enviar enlaces en este grupo.')

def add_warning(update: Update, user_id: int, context: CallbackContext) -> None:
    # Incrementar el contador de advertencias
    if user_id in user_warnings:
        user_warnings[user_id] += 1
    else:
        user_warnings[user_id] = 1

    warnings = user_warnings[user_id]

    if warnings == 3:
        # Baneo temporal
        context.bot.restrict_chat_member(
            chat_id=update.message.chat.id,
            user_id=user_id,
            until_date=int(time.time()) + 1200,  # 20 minutos
            permissions={
                'can_send_messages': False,
                'can_send_media_messages': False,
                'can_send_other_messages': False,
                'can_add_web_page_previews': False,
            }
        )
        update.message.reply_text(f'Usuario {update.message.from_user.first_name} ha sido baneado temporalmente por 20 minutos.')

    elif warnings >= 5:
        # Expulsar del grupo
        context.bot.kick_chat_member(chat_id=update.message.chat.id, user_id=user_id)
        del user_warnings[user_id]  # Eliminar advertencias
        update.message.reply_text(f'Usuario {update.message.from_user.first_name} ha sido expulsado del grupo.')

def main() -> None:
    # Reemplaza 'YOUR_TOKEN_HERE' con el token de tu bot
    updater = Updater("7638517033:AAEG-4IXKTUorrVJZN8ymW5F923pqrnezhI")

    # Obtén el despachador para registrar manejadores
    dispatcher = updater.dispatcher

    # Registra los comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Registra el manejador de mensajes para filtrar enlaces
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_links))

    # Inicia el bot
    updater.start_polling()

    # Ejecuta el bot hasta que presiones Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
  
