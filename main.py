from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "6577811093:AAHVZJbqAoPPRo-IfASoIkwtX-9ZT2f4e1g"
USERNAME = "@sciacca_benzina_bot"

informazioni = ["", "Inserisci il tipo di carburante:", "Inserisci la capacità del tuo serbatoglio:", "Inserisci la distanza massima che vuoi percorrere:"]
informazioniBack = ["", "Inserisci il tipo di carburante:", "Inserisci la capacità del tuo serbatoglio:", "Inserisci la distanza massima che vuoi percorrere:"]
# 0: nome; 1: tipo carburante; 2: capacità; 3: distanza max

counter: int = 0     #counter per sapere quanti dati sonon già stati inseriti
latitudine: float = None
longitudine: float = None

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter
    global informazioni
    global informazioniBack
    global latitudine
    global longitudine

    counter = 0
    informazioni = list(informazioniBack)
    latitudine = None
    longitudine = None

    await update.message.reply_text("Benvenuto. Inserisci il tuo nome:")

# Responses
def handle_response(messaggio: Update) -> Update:
    global counter
    global informazioni
    global latitudine
    global longitudine

    if counter < 4:
        informazioni[counter] = messaggio.message.text
        counter += 1
        return (informazioni[counter] if counter != 4 else "Inserisci la tua posizione:")
    elif messaggio.message.location != None:
        latitudine = messaggio.message.location.latitude
        longitudine = messaggio.message.location.longitude
        print("lat:" + str(latitudine) + " lon:" + str(longitudine))
    else:
        return "errore"

# Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print (f"User ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type == "group":
        if USERNAME in text:
            new_text: str = text.replace(USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(update)

    
    print("Bot:", response)
    await update.message.reply_text(response)

# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(KeyboardInterrupt())
    # Messages
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=5)