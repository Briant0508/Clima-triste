import telebot, yt_dlp, os
from keep_alive import mantener_vivo

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
mantener_vivo()

def descargar(url, calidad=None, mp3=False):
    opts = {
        'quiet': True,
        'geo_bypass': True,
        'outtmpl': 'media.%(ext)s'
    }
    if mp3:
        opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }]
        })
    else:
        opts['format'] = f'bestvideo[height<={calidad}]+bestaudio/best[height<={calidad}]'
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, (
        "👋 *¡Bienvenido al Bot Descargador!* 🎬\n\n"
        "📥 Envía cualquier enlace de YouTube, TikTok, Instagram o Twitter\n"
        "y elige cómo quieres descargarlo: video en calidad media o solo audio MP3."
    ), parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("http"))
def recibir_enlace(msg):
    url = msg.text.strip()
    markup = telebot.types.InlineKeyboardMarkup()
    for q in ['360', '240', '144', 'mp3']:
        label = f"{q}p" if q != "mp3" else "🎧 MP3"
        markup.add(telebot.types.InlineKeyboardButton(label, callback_data=f"{q}:{url}"))
    bot.send_message(msg.chat.id, "📌 Elige la calidad de descarga:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    q, url = c.data.split(":")
    try:
        if q == "mp3":
            descargar(url, mp3=True)
            with open("media.mp3", "rb") as f: bot.send_audio(c.message.chat.id, f)
            os.remove("media.mp3")
        else:
            descargar(url, calidad=int(q))
            with open("media.mp4", "rb") as f: bot.send_video(c.message.chat.id, f)
            os.remove("media.mp4")
    except:
        bot.send_message(c.message.chat.id, (
            "❌ No se pudo completar la descarga.\n"
            "🔍 Verifica el enlace o intenta con otra calidad."
        ))

bot.polling()