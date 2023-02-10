from flask import Flask, jsonify
import logging

# Global variables
keys = {"keys": []}

# Configure application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

@app.route('/')
def index():
    return 'Hello World', 200

@app.route('/jwks')
def jwks():
    # This is the JWK that is the public key used to valdate the JWT sent in the authenication request signed with the private key
    key = [
        {
            "kty": "RSA",
            "e": "AQAB",
            "use": "sig",
            "alg": "RS256",
            "n": "sxIfIYv04dq9_NIkh-HNvNiweWgGw_N7VCsqHf51pxQ5Fk2e6SwmyLC4wM11XYFAugx_DaXq_7koKiDEPRh-n9Gnb4bhg7PokuWM4482IhB9Rn18mXHzTpfCEDdXKiJJpHIYXiXGp5iF89LvK1eRO--9qE7P7Rhfpah-W0nXwiaqUMOpOqPQwY8Dsi4H5bL8U2yXhqODITg0FPcorB8S9us8GbI1oZ3gcqsRs2_JG0It8vnrul8ptWfN8EUAp1eFeoy4nWrhstkrIgNEeOMmVDsSn79Scbvf-h95ow_YfFJVMqrai_rNGeAjQ5vzwZcCRJfVo59WELbFySpjBMRrGQ"
        }
    ]
    keys["keys"] = key

    return jsonify(keys), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
