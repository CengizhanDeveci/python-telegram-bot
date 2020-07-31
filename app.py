from telegram.ext import Updater, CommandHandler
import requests
from lxml import html


def start(bot,update):
    
    bot.send_message(chat_id=update.message.chat_id, text=f"Hi. What can I do for you? You can use /help for commands.")

def help(bot, update):
    update.message.reply_text("""You can use
    /send_news to get bbc most read news and
    /wiki to get today's featured article
    """)

def wiki(bot, update):
    page = requests.get("https://en.wikipedia.org/wiki/Main_Page")
    tree = html.fromstring(page.text)
    wikiarticle = tree.xpath('//*[@id="mp-tfa"]/p/b[2]/a')
    update.message.reply_text("https://en.wikipedia.org" + wikiarticle[0].attrib["href"])


def send_news(bot,update):
    
    page = requests.get("https://www.bbc.com/news")
    tree = html.fromstring(page.text)

    news_list = list()
    for i in range(1, 11):
        elem = tree.xpath("//li[@data-entityid='most-popular-read-{}']//a".format(i))
        if elem != []:
            news_list.append(elem[0])

    if len(news_list) == 0:
        update.message.reply_text("Opps!!")
        return
    else:
        update.message.reply_text("Most read news for you!!")
    for new in news_list:
        update.message.reply_text("https://www.bbc.com" + new.attrib["href"])




def main():
    updater = Updater(token=YOUR_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('send_news',send_news))
    dp.add_handler(CommandHandler('wiki',wiki))


    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
