from datetime import datetime
import requests
import datetime
import telebot
from auth_data import token, weather_token


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend!")

    @bot.message_handler(commands=['weather'])
    def send_weather(message):
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text.split()[1]}&appid={weather_token}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

            bot.send_message(
                message.chat.id,
                f"city: {city}\n"
                f"temperature: {cur_weather}\n"
                f"humidity: {humidity}\n"
                f"pressure: {pressure}\n"
                f"wind: {wind}\n"
                f"sunrise: {sunrise_timestamp}\n"
                f"sunset: {sunset_timestamp}"
            )
        except Exception as ex:
            print(f"[ERROR] {ex}")
            bot.send_message(
                message.chat.id,
                "Damn... something wrong with command '/weather'!"
            )

    @bot.message_handler(content_types=["text"])
    def send_btc_price(message):
        if message.text.lower() == "price":
            try:
                req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
                response = req.json()
                sell_price = response["btc_usd"]["sell"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}$"
                )
            except Exception as ex:
                print(f"[ERROR] {ex}")
                bot.send_message(
                    message.chat.id,
                    "Damn... something wrong!"
                )
        else:
            bot.send_message(message.chat.id, "Unknown command")

    bot.polling()


def main():
    telegram_bot(token)


if __name__ == '__main__':
    main()
