import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# 🌟 Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "👋 ¡Hola! Soy tu bot del clima.\n\n"
        "Puedes usar los siguientes comandos:\n"
        "• /clima [ciudad] — Consulta el clima actual\n"
        "• /ayuda — Ver cómo usar el bot\n"
        "• /info — Saber quién soy\n"
    )
    await update.message.reply_text(mensaje)

# 🌤 Comando /clima
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE.args:
        await update.message.reply_text("❗️ Por favor, escribe una ciudad. Ejemplo: /clima Madrid")
        return

    ciudad = " ".join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_API_KEY}&units=metric&lang=es"

    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            await update.message.reply_text("⚠️ Ciudad no encontrada.")
            return

        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        humedad = response["main"]["humidity"]
        viento = response["wind"]["speed"]

        mensaje = (
            f"🌤 Clima en *{ciudad.title()}*:\n"
            f"🌡 Temperatura: {temp}°C\n"
            f"📝 Descripción: {desc}\n"
            f"💧 Humedad: {humedad}%\n"
            f"💨 Viento: {viento} m/s"
        )
        await update.message.reply_markdown(mensaje)

    except Exception as e:
        await update.message.reply_text("❌ Error al obtener el clima.")

# 🆘 Comando /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "📚 *Cómo usar el bot:*\n\n"
        "• Usa `/clima [ciudad]` para saber el clima actual.\n"
        "• Ejemplo: `/clima Buenos Aires`\n"
        "• Si tienes dudas, escribe `/info` para saber más."
    )
    await update.message.reply_markdown(mensaje)

# ℹ️ Comando /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "🤖 *Bot del Clima*\n"
        "Desarrollado por Briant.\n"
        "Usa datos de OpenWeatherMap para mostrar el clima actual.\n"
        "¡Gracias por usarme!"
    )
    await update.message.reply_markdown(mensaje)

# 🚀 Configuración del bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("clima", clima))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("info", info))

if __name__ == "__main__":
    app.run_polling()