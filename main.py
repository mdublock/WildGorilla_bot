import telebot
from extensions import Converter, APIException
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\nДля вывода списка доступных валют введите команду /values.")

@bot.message_handler(commands=['values'])
def send_values(message):
    bot.reply_to(message, "Доступные валюты: \nUSD - доллар США\nEUR - евро\nRUB - российский рубль")

@bot.message_handler(content_types=['text'])
def get_price(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException("Неправильный формат запроса, введите команду /help для получения инструкций.")

        base, quote, amount = values
        result = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка конвертации валюты:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка выполнения команды:\n{e}")
    else:
        bot.reply_to(message, f"{amount} {base} = {result} {quote}")

bot.polling(none_stop=True)
