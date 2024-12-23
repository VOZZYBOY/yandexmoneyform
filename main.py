import hashlib
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

SHOP_ID = 'your_shop_id'
SHOP_SECRET = 'your_secret_key'
SCID = 'your_scid'
RETURN_URL = 'https://yourwebsite.com/return_url'

@app.route('/')
def index():
    return render_template('payment_form.html')

def generate_signature(params, secret_key):
    signature_string = ''.join([f'{k}={v}' for k, v in sorted(params.items())]) + secret_key
    return hashlib.sha256(signature_string.encode('utf-8')).hexdigest()

@app.route('/pay', methods=['POST'])
def pay():
    amount = request.form['amount']
    order_id = request.form['order_id']

    params = {
        'shop_id': SHOP_ID,
        'scid': SCID,
        'sum': amount,
        'order_number': order_id,
        'return_url': RETURN_URL
    }

    signature = generate_signature(params, SHOP_SECRET)
    params['signature'] = signature

    response = requests.post('https://yoomoney.ru/eshop/confirmation', data=params)

    if response.status_code == 200:
        return redirect(response.text)
    else:
        return 'Ошибка при отправке запроса'

if __name__ == '__main__':
    app.run(debug=True)
