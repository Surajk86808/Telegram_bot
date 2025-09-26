Telegram Bot Guide: From Local PC to 24/7 Deployment
This guide will walk you through every step needed to get your Python Telegram bot running, first on your own computer and then on a free cloud service so it's always online.

Part 1: Running the Bot on Your Local PC
This is for testing and development. The bot will only work as long as the script is running on your computer.

Prerequisites:

Python 3.8 or newer installed on your computer.

A Telegram Bot Token from BotFather.

Step 1: Set Up Your Project

Create a new folder for your project (e.g., my-telegram-bot).

Place the telegram_bot.py and requirements.txt files inside this folder.

Step 2: Create a Virtual Environment (Highly Recommended)
A virtual environment keeps your project's libraries separate from others on your system.

Open a terminal or command prompt in your project folder.

Run: python -m venv venv

Activate it:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Step 3: Install Required Libraries
With your virtual environment active, install the libraries listed in requirements.txt:

pip install -r requirements.txt

Step 4: Add Your Bot Token
Open telegram_bot.py and replace "YOUR_BOT_TOKEN_HERE" with your actual bot token from BotFather.

Step 5: Run the Bot!
In your terminal, simply run the script:

python telegram_bot.py

You should see "Bot is running...". Now, go to Telegram, find your bot, and send the /start command. It should work! Press CTRL+C in the terminal to stop the bot.

Part 2: Deploying Your Bot to Run 24/7 (For Free)
To make your bot available all the time, you need to host it on a server. We'll use Render.com, which offers a free tier perfect for this kind of bot.

Prerequisites:

A free GitHub account.

A free Render.com account.

Step 1: Prepare Your Code for Deployment

IMPORTANT: In telegram_bot.py, remove your hardcoded bot token. The code I provided already looks for an "environment variable," which is a secure way to handle secrets. Make sure the line looks like this:
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

Create a new repository on GitHub and upload your telegram_bot.py and requirements.txt files.

Step 2: Deploy on Render.com

Log in to your Render dashboard and click "New +" -> "Web Service".

Connect your GitHub account and select the repository you just created.

On the settings page, fill in the details:

Name: Give your bot a unique name (e.g., my-cool-telegram-bot).

Region: Choose a region close to you.

Branch: main (or your default branch).

Runtime: Python 3.

Build Command: pip install -r requirements.txt

Start Command: python telegram_bot.py

Instance Type: Make sure to select the Free plan.

Scroll down to "Advanced" and click "Add Environment Variable". This is the crucial step for adding your token securely.

Key: TELEGRAM_BOT_TOKEN

Value: YOUR_ACTUAL_BOT_TOKEN (paste your token here)

!

Click "Create Web Service". Render will now build and deploy your bot. You can watch the progress in the logs. Once it says "Bot is running...", your bot is live and will stay online!

Part 3: Connecting to n8n (or any other service)
Your code comments mentioned n8n. The provided telegram_bot.py is already set up to send data to n8n webhooks.

In n8n: Create a new workflow and add a "Webhook" node as the trigger. Copy the Test URL it gives you.

In Render: Go to your service's "Environment" tab. Add two more environment variables:

N8N_FILE_WEBHOOK_URL: Paste the webhook URL for your file-handling workflow.

N8N_MESSAGE_WEBHOOK_URL: Paste the webhook URL for your message-handling workflow.

Render will automatically restart your bot with the new variables. Now, when you send a message or file to your bot, it will not only reply but also forward the data to your n8n workflows!