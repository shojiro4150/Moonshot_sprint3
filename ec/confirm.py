import requests,json
import paypayopa
import time
from .local_settings import *
from .policycreate import create_session_and_login
from .forms import GetInsuranceForm

def DetailConfirm():

    #policyの取得
    session = create_session_and_login()
    policyLocator_str = str(GetInsuranceForm.policyLocator)
    response = session.get(
        'http://api.sandbox.socotra.com/policy/'+ policyLocator_str,
    )
    print(response)

    #policy情報の取り出し
    found_policy = response.json()
    policy_info = found_policy['characteristics']

    #forms情報の取り出し
    #policyLocator_str = str(GetInsuranceForm.policyLocator)

    #保険料の取り出し
    grossPremium = int(policy_info[0]["grossPremium"])
    print(grossPremium)

    #payapyでの支払い
    client = paypayopa.Client(auth=(API_KEY, API_SECRET), production_mode=False)
    client.set_assume_merchant(MERCHANT_ID)

    # requestの送信情報について
    # => https://www.paypay.ne.jp/opa/doc/jp/v1.0/preauth_capture#operation/createAuth
    request = {
        "merchantPaymentId": round(time.time()), # => 加盟店発番のユニークな決済取引ID
        "codeType": "ORDER_QR",
        "redirectUrl": "http://moonshot.shjr.jp/", # => ここを任意のフロントアプリ
        "redirectType": "WEB_LINK",
        "orderDescription":policyLocator_str,
        "orderItems": [{
            "name": policyLocator_str,
            "category": "pasteries",
            "quantity": 1,
            "productId": "67678",
            "unitPrice": {
                "amount": grossPremium,
                "currency": "JPY"
            }
        }],
        "amount": {
            "amount": grossPremium,
            "currency": "JPY"
        },
    }

    response = client.Code.create_qr_code(request)
    paypay_url = response['data']['url']

    print(paypay_url)

    return(found_policy,paypay_url)