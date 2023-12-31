import requests
import telegram
import io
import hashlib

def check_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def get_file_hash(file_path):
    with io.open(file_path, "rb") as f:
        hash_digest = hashlib.sha256()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_digest.update(chunk)
        return hash_digest.hexdigest()

def handle_message(update, context):
    file_id = update.message.document.file_id
    file = context.bot.getFile(file_id)
    file_content = file.file_path

    file_hash = get_file_hash(file_content)

    if file_hash not in scanned_files:
        scanned_files[file_hash] = True

        for url in urls:
            result, line = check_url(url)
            if result:
                context.bot.send_message(chat_id=update.effective_chat.id, text=line)  # Atualização aqui

    if update.message.text.startswith("/cmd") or update.message.text.startswith("/ajuda"):
        commands = {
            "/cmd": "Mostra todos os comandos do bot",
            "/addurl": "Adiciona uma URL à lista de URLs válidas.\n\nExemplos:\n\n* /addurl https://www.example.com\n* /addurl 123456789",
            "/removeurl": "Remove uma URL da lista de URLs válidas.\n\nExemplos:\n\n* /removeurl https://www.example.com\n* /removeurl 123456789",
            "/addchannel": "Adiciona um canal para o bot entrar.\n\nExemplos:\n\n* /addchannel @my_channel\n* /addchannel 123456789",
        }
        context.bot.send_message(chat_id=update.effective_chat.id, text="Comandos disponíveis:\n" + "\n".join(f"* {key}: {value}" for key, value in commands.items()))  # Atualização aqui

    if update.message.text == "/addurl":
        url = update.message.reply_to_message.text
        urls.add(url)
        context.bot.send_message(chat_id=update.effective_chat.id, text="URL adicionada com sucesso.")  # Atualização aqui

    if update.message.text == "/removeurl":
        url = update.message.reply_to_message.text
        urls.remove(url)
        context.bot.send_message(chat_id=update.effective_chat.id, text="URL removida com sucesso.")  # Atualização aqui

    if update.message.text.startswith("/addchannel"):
        channel_id = update.message.reply_to_message.text
        if channel_id.startswith("@"):
            channel_id = channel_id[1:]
        channels.add(channel_id)
        context.bot.join_chat(channel_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Canal adicionado com sucesso.")  # Atualização aqui

updater = telegram.Updater(token="6655452268:AAF3EiLH28rZd9_1QRdGJHq6DW8LYbmyWXY", use_context=True)  # Atualização aqui
dispatcher = updater.dispatcher  # Atualização aqui
dispatcher.add_handler(telegram.MessageHandler(telegram.Filters.document, handle_message))
updater.start_polling()
