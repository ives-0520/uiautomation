# filepath: c:\Users\Administrator\Desktop\APP_UI_AUTO\utils\account_generate.py

import random
import string
import logging

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com","ipwangxin.cn"]
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_random_phone():
    phone_number = "+55" + ''.join(random.choices(string.digits, k=10))
    return phone_number

# Example usage
if __name__ == "__main__":
    logging.info(f"Random Email: {generate_random_email()}")
    logging.info(f"Random Phone: {generate_random_phone()}")