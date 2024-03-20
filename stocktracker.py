from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

TOKEN: final = 'TELEGRAM_BOT_KEY'
BOT_USERNAME: final = '@stocksavvy_bot'
ALPHA_VANTAGE_API_KEY: final = 'API_KEY'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to Stock Savvy! \nType /stock <symbol> to get the current price of a stock.')

async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0]
        price_data = get_stock_price(symbol)
        if price_data:
            await update.message.reply_text(price_data)
        else:
            await update.message.reply_text('Stock data not found for the specified symbol.')
    except IndexError:
        await update.message.reply_text('Please provide a stock symbol.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Welcome to StockTrackerBot! Here are the available commands:\n"
        "/start - Start the bot and get welcome message\n"
        "/stock <symbol> - Get the current price of a stock\n"
        "/help - Learn what a stock symbol is"
        "/about - About Stock Savvy Bot\n"
    )
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "Stock Savvy 1.0\n"
        "This bot provides current stock price information for publicly traded companies.\n"
        "Created by Rudransh Das\n"
        "Check out my portfolio: [https://rudransh.rf.gd]"
    )
    await update.message.reply_text(about_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    explanation_text = (
        "A stock symbol is a unique identifier assigned to publicly traded shares of a particular company.\n"
        "For example:\n"
        "Apple Inc.'s stock symbol is \"AAPL\"\n"
        "Microsoft Corporation's stock symbol is \"MSFT\"\n"
        "Alphabet Inc.'s stock symbol is \"GOOGL\""
    )
    await update.message.reply_text(explanation_text)

def get_stock_price(symbol: str) -> str:
    base_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(base_url)
    data = response.json()
    if 'Global Quote' in data:
        price_info = data['Global Quote']
        return (f"Stock Symbol: {symbol}\n"
                f"💰 Price: {price_info['05. price']}\n"
                f"📈 Open: {price_info['02. open']}\n"
                f"📉 Previous Close: {price_info['08. previous close']}")
    else:
        return ''

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('stock', stock_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about_command))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
