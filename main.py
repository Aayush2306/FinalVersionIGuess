import telebot
import requests
import json

Api_Key = "5887063651:AAFevQWanmPYhbcEuFCkC_5dTn5QwypKJ1o"
bot = telebot.TeleBot(Api_Key)
freeKey = "EK-cgMkq-f79VYYW-u1JY5"
addy = []


@bot.message_handler(commands=["list"])
def greetings(message):
  global addy
  text = "Here's a list of links:\n"
  if not addy:
    bot.send_message(message.chat.id,
                     f"Send Contract address first u dumb bitch")
    return
  if addy:
    for i, link in enumerate(addy):
      text += f"{i + 1}. https://etherscan.io/address/{link}\n \n"

  bot.send_message(message.chat.id, text)
  addy = []


@bot.message_handler(commands=['start'])
def greet(message):
  bot.send_message(
    message.chat.id,
    "Hey Welcome To Smart Wallet AI Made by @WenCGWenCMC \n Use /ca to search the contract \n Use /list to get list of wallets after you searched a ca "
  )


def get_holders(array_of_objects, key):
  return [obj[key] for obj in array_of_objects]


def get_contract_holders(message):
  global addy
  contract_address = message.text.split(" ")[1]
  url = f"https://api.ethplorer.io/getTopTokenHolders/{contract_address}?apiKey={freeKey}&limit=50"
  response_API = requests.get(url)
  data = response_API.text
  real_data = json.loads(data)
  holders = get_holders(real_data['holders'], "address")
  print(len(holders))
  tx_counts = get_tx_counts(holders)
  less_than_10 = [wallet for wallet, count in tx_counts.items() if count < 11]
  addy = less_than_10
  less_than_5 = [wallet for wallet, count in tx_counts.items() if count < 5]
  #print(less_than_5)
  less_than_3 = [wallet for wallet, count in tx_counts.items() if count < 4]
  lenLessThan3 = len(less_than_3)
  lenLessThan5 = len(less_than_5)
  lenLessThan10 = len(less_than_10)
  print(lenLessThan10)
  percentage = (lenLessThan10 / len(holders)) * 100
  print(percentage)
  round_percentage = round(percentage, 2)
  bot.send_message(
    message.chat.id,
    f"There are {lenLessThan10} wallets with less than 10 transactions.\n\nThere are {lenLessThan5} wallets with less than 5 transactions.\n\n There are {lenLessThan3} wallets which only bought this token.\n\n Total % of new wallets are {round_percentage}% "
  )
  bot.send_message(
    message.chat.id,
    f"Press /list to get list of the holders with less than 10 transcation")


def get_tx_count(address):
  url = f"https://mainnet.infura.io/v3/c1f653384020470d942fdd4d8eb97795"
  headers = {'Content-Type': 'application/json'}
  payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "eth_getTransactionCount",
    "params": [address, "latest"]
  }
  response = requests.post(url, headers=headers, data=json.dumps(payload))
  result = response.json()['result']
  return int(result, 16)


def get_tx_counts(addresses):
  tx_counts = {}
  for address in addresses:
    tx_counts[address] = get_tx_count(address)
  return tx_counts


@bot.message_handler(commands=["ca"])
def echo_message(message):
  print(message.text)
  user_name = message.from_user.first_name
  if not message.text.split(" ")[1].startswith("0x"):
    bot.send_message(
      message.chat.id,
      f"Hey Thats not a Ca i know you have nothing to do in life instead of shitcoins but dont waste my time"
    )
  else:
    bot.send_message(
      message.chat.id,
      f"Hey! {user_name} Searching Your Query Might take up to 2 mins! ")
    get_contract_holders(message)


bot.polling()
