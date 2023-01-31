import telebot
import requests
import json

Api_Key = "5886161991:AAEgtfANerUZWylTLlvFtptPX2v3iNBHja0"
bot = telebot.TeleBot(Api_Key)
freeKey = "EK-cgMkq-f79VYYW-u1JY5"
addy = []


@bot.message_handler(commands=['start'])
def greet(message):
  bot.send_message(message.chat.id, "Paste A Ethereum Contract Address")


@bot.message_handler(commands=['addy'])
def greetings(message):
  global addy
  text = "Here's a list of links:\n"
  if not addy:
    bot.send_message(message.chat.id,
                     f"Seach a contract address first u Dumb Bitch ")
    return
  if addy:
    for i, link in enumerate(addy):
      text += f"{i + 1}. {link}\n \n"

  bot.send_message(message.chat.id, text)
  addy = []


def get_holders(array_of_objects, key):
  return [obj[key] for obj in array_of_objects]


def get_total_tx_from_holders(holders, message):
  sum = 0
  special_alpha = 0
  giga_chad = 0
  global addy
  for index, value in enumerate(holders):
    url = f"https://api.ethplorer.io/getAddressInfo/{value}?apiKey={freeKey}&showETHTotals=false"
    response_API = requests.get(url)
    data = response_API.text
    trans = json.loads(data)
    total_tx = trans['countTxs']
    if 1 < total_tx < 11:
      sum += 1
      holder = f"https://etherscan.io/address/{trans['address']}"
      global addy
      addy.append(holder)
    if 1 < total_tx < 7:
      special_alpha += 1
    if 1 < total_tx < 5:
      giga_chad += 1
    if index == len(holders) - 1:
      print(addy)
      percentage = (sum / len(holders)) * 100
      round_percentage = round(percentage, 2)
      bot.send_message(
        message.chat.id,
        f"There are {sum} wallets with less than 10 transactions.\nThere are {special_alpha} wallets with less than 5 transactions.\n There are {giga_chad} wallets which only bought this token.\n Total % of new wallets are {round_percentage}% "
      )
      bot.send_message(
        message.chat.id,
        f"Press /addy to get list of the holders with less than 10 transcation"
      )


def get_contract_holders(message):
  contract_address = message.text
  url = f"https://api.ethplorer.io/getTopTokenHolders/{contract_address}?apiKey={freeKey}&limit=50"
  response_API = requests.get(url)
  data = response_API.text
  real_data = json.loads(data)
  holders = get_holders(real_data['holders'], "address")
  get_total_tx_from_holders(holders[1:], message)


@bot.message_handler(func=lambda message: message.text.startswith("0x"))
def echo_message(message):
  user_name = message.from_user.first_name
  bot.send_message(
    message.chat.id,
    f"Hey! {user_name} Searching Your Query Might take up to 2 mins! ")
  get_contract_holders(message)


@bot.message_handler(func=lambda message: True)
def echoo_message(message):
  user_name = message.from_user.first_name
  bot.send_message(
    message.chat.id,
    f"Hey! {user_name} U Dumb Bozo Thats Not A Contract Address ")


bot.polling()
