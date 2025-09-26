import os
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# It's best practice to get the token from an environment variable
# for security reasons. You'll set this up during deployment.
from dotenv import load_dotenv # <-- This library is important

# Load variables from your .env file into the environment
load_dotenv()

# Get the token SECURELY from the environment. No more token in the code!
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
N8N_FILE_WEBHOOK = os.getenv("N8N_FILE_WEBHOOK_URL")
N8N_MESSAGE_WEBHOOK = os.getenv("N8N_MESSAGE_WEBHOOK_URL")
# --- Command Handlers ---

# This function is called when a user sends the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user and shows the main options."""
    user = update.effective_user
    greeting_message = f"👋 Hello {user.first_name}! Welcome to your bot."
    
    # Define the buttons that will be shown to the user
    keyboard = [["📂 Upload File", "📝 Send Message"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        one_time_keyboard=True, # The keyboard disappears after one use
        resize_keyboard=True,   # Makes the keyboard fit the screen nicely
        input_field_placeholder="Please choose an option..."
    )
    
    await update.message.reply_text(greeting_message)
    await update.message.reply_text(
        "What would you like to do?",
        reply_markup=reply_markup
    )

# --- Message Handlers ---

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the user's choice from the main keyboard."""
    text = update.message.text
    if text == "📂 Upload File":
        await update.message.reply_text(
            "Please upload your file now. 📤",
            reply_markup=ReplyKeyboardRemove() # Removes the custom keyboard
        )
    elif text == "📝 Send Message":
        await update.message.reply_text(
            "Please type your message now. 🖊️",
            reply_markup=ReplyKeyboardRemove()
        )

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles a generic text message and forwards it to an n8n webhook if configured."""
    text = update.message.text
    user_info = update.effective_user
    
    response_message = f"✅ Got your message:\n\n\"{text}\""
    await update.message.reply_text(response_message)

    # --- n8n Integration for Messages ---
    if N8N_MESSAGE_WEBHOOK:
        # We will send the message data to your n8n webhook
        payload = {
            "text": text,
            "user_id": user_info.id,
            "first_name": user_info.first_name,
            "username": user_info.username
        }
        try:
            # Using the 'requests' library to send a POST request
            response = requests.post(N8N_MESSAGE_WEBHOOK, json=payload)
            response.raise_for_status() # Raises an error for bad responses (4xx or 5xx)
            await update.message.reply_text("🚀 Message successfully sent to your workflow!")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to n8n: {e}")
            await update.message.reply_text("⚠️ Could not connect to the n8n workflow.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles a file upload and forwards it to an n8n webhook if configured."""
    document = update.message.document
    user_info = update.effective_user
    
    await update.message.reply_text(f"📂 Thanks! You uploaded: {document.file_name}")

    # --- n8n Integration for Files ---
    if N8N_FILE_WEBHOOK:
        # Download the file from Telegram's servers
        file = await document.get_file()
        file_content = await file.download_as_bytearray()
        
        # Prepare the data to be sent
        files = {'file': (document.file_name, file_content, document.mime_type)}
        data = {
            "user_id": user_info.id,
            "first_name": user_info.first_name,
            "username": user_info.username
        }

        try:
            # Send the file as a multipart/form-data POST request
            response = requests.post(N8N_FILE_WEBHOOK, files=files, data=data)
            response.raise_for_status()
            await update.message.reply_text("🚀 File successfully sent to your workflow!")
        except requests.exceptions.RequestException as e:
            print(f"Error sending file to n8n: {e}")
            await update.message.reply_text("⚠️ Could not send the file to the n8n workflow.")


# --- Main Bot Logic ---

def main():
    """Starts the bot."""
    print("🚀 Starting bot...")
    
    # Create the Application instance
    app = Application.builder().token(TOKEN).build()

    # Add handlers for different commands and message types
    app.add_handler(CommandHandler("start", start))
    
    # Handler for the keyboard button presses
    app.add_handler(MessageHandler(filters.Regex('^(📂 Upload File|📝 Send Message)$'), handle_choice))
    
    # Handler for file uploads (documents)
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Handler for any other text message that isn't a command or a button press
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Start the bot and wait for messages
    print("🤖 Bot is running and listening for messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
