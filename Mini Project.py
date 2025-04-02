from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.ext import MessageHandler, filters
import csv
import os
from fpdf import FPDF  # pip install fpdf

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey, This is Mason's Bot to help you learn faster")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm here to help! Try typing /start or say hi!")

async def upload_instruction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Please upload a .txt file with one word per line. I’ll send back a PDF with example sentences and explanations! 📄✨")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("/menu command received - displaying reply keyboard")
    keyboard = [["📥 Upload Word List", "📄 Generate PDF"], ["➕ Add Word", "➖ Remove Word"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "greet":
        await query.edit_message_text("Hey there! 👋 Nice to see you.")
    elif query.data == "help":
        await query.edit_message_text(text="This is the help section. Type /start to begin!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "This is the text to see the message 👋":
        await update.message.reply_text("Hi there! 👋 You pressed the first button.")
    elif text == "Tey Keith, **** these niggas up 🆘":
        await update.message.reply_text("Beat dropping in 3... 2... 1... 🔥")
    elif text == "New WordList 📖":
        await update.message.reply_text("Here's a fresh word list just for you! 📚✨")
    elif text == "📥 Upload Word List":
        await update.message.reply_text("You chose to upload a word list. Please send a .txt file now.")
    elif text == "📄 Generate PDF":
        await update.message.reply_text("Upload your list of words to receive a PDF with explanations. 🧾")
    elif text == "➕ Add Word":
        await update.message.reply_text("Feature coming soon: Add new words to your personal list.")
    elif text == "➖ Remove Word":
        await update.message.reply_text("Feature coming soon: Remove words from your personal list.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document:
        file = await document.get_file()
        file_path = f"{document.file_unique_id}.txt"
        await file.download_to_drive(file_path)

        # Read words from uploaded file
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            words = [line.strip() for line in f if line.strip()]

        # Generate PDF file
        pdf_path = f"{document.file_unique_id}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Word List with Examples and Explanations".encode("latin-1", "replace").decode("latin-1"), ln=True, align="C")
        pdf.ln(10)

        for word in words:
            pdf.cell(200, 10, txt=f"Word: {word}".encode("latin-1", "replace").decode("latin-1"), ln=True)
            pdf.cell(200, 10, txt=f"Example: Example sentence for {word}".encode("latin-1", "replace").decode("latin-1"), ln=True)
            pdf.cell(200, 10, txt=f"Explanation: Explanation of {word}".encode("latin-1", "replace").decode("latin-1"), ln=True)
            pdf.ln(5)

        pdf.output(pdf_path)

        # Send the PDF file back to user
        with open(pdf_path, "rb") as pdf_file:
            await update.message.reply_document(document=InputFile(pdf_file, filename="word_list.pdf"))

        # Clean up
        os.remove(file_path)
        os.remove(pdf_path)

app = ApplicationBuilder().token("8046820293:AAE7aomlhoMspflsuX3T2A_i_qq4MM86A_Y").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("upload", upload_instruction))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.run_polling()