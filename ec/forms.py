from django import forms
from django.core.mail import EmailMessage

from .models import Diary
from .policycreate import create_session_and_login

class GetInsuranceForm(forms.Form):
    name = forms.CharField(label='ご契約者名', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    beergarden_name = forms.CharField(label='店舗名', max_length=30)
    prefecture = forms.fields.ChoiceField(
        choices = (
            ("北海道","北海道"),
            ("青森","青森"),
            ("岩手","岩手"),
            ("宮城","宮城"),
            ("秋田","秋田"),
            ("山形","山形"),
            ("福島","福島"),
            ("茨城","茨城"),
            ("栃木","栃木"),
            ("群馬","群馬"),
            ("埼玉","埼玉"),
            ("千葉","千葉"),
            ("東京","東京"),
            ("神奈川","神奈川"),
            ("新潟","新潟"),
            ("富山","富山"),
            ("石川","石川"),
            ("福井","福井"),
            ("山梨","山梨"),
            ("長野","長野"),
            ("岐阜","岐阜"),
            ("静岡","静岡"),
            ("愛知","愛知"),
            ("三重","三重"),
            ("滋賀","滋賀"),
            ("京都","京都"),
            ("大阪","大阪"),
            ("兵庫","兵庫"),
            ("奈良","奈良"),
            ("和歌山","和歌山"),
            ("鳥取","鳥取"),
            ("島根","島根"),
            ("岡山","岡山"),
            ("広島","広島"),
            ("山口","山口"),
            ("徳島","徳島"),
            ("香川","香川"),
            ("愛媛","愛媛"),
            ("高知","高知"),
            ("福岡","福岡"),
            ("佐賀","佐賀"),
            ("長崎","長崎"),
            ("熊本","熊本"),
            ("大分","大分"),
            ("宮崎","宮崎"),
            ("鹿児島","鹿児島"),
            ("沖縄","沖縄")
        ),
        label ='都道府県',
        initial='北海道',
        required=True,
        widget=forms.widgets.Select()
    )
    sales = forms.CharField(label='売上金額')
    message = forms.CharField(label='備考', widget=forms.Textarea,required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-12'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力してください。'

        self.fields['beergarden_name'].widget.attrs['class'] = 'form-control col-12'
        self.fields['beergarden_name'].widget.attrs['placeholder'] = '店舗名を入力してください。'

        self.fields['prefecture'].widget.attrs['class'] = 'form-control col-12'
        self.fields['prefecture'].widget.attrs['placeholder'] = '所在地を入力してください。'

        self.fields['sales'].widget.attrs['class'] = 'form-control col-12'
        self.fields['sales'].widget.attrs['placeholder'] = '１日の売上金額を入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = '備考をここに入力してください。'

    def create_exposure(self):
        # Create an exposure with two perils
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        #ymd = self.cleaned_data['ymd']
        beergarden_name = self.cleaned_data['beergarden_name']
        prefecture = self.cleaned_data['prefecture']
        sales = self.cleaned_data['sales']
        message = self.cleaned_data['message']

        # Create an exposure with two perils
        exposure_values = {'prefecture': prefecture,
                        'store_location': 'test',
                        'store_name': beergarden_name,
                        'sales': sales,
                        }

        exposure = {'exposureName': 'beer garden',
                    'fieldValues': exposure_values,
                    'perils': [{'name': ' unexpected low temperature'}]
                    }
        
        #form情報を他クラスで利用
        GetInsuranceForm.name = name
        GetInsuranceForm.email = email

        return exposure # policyLocatorを追加して返す

        # ホスト名取得（引数）
        # Socotraログイン
    def send_socotra(self):
        session = create_session_and_login()
        policyholder_locator = '3db5507e-d66f-406b-be92-027b89d2b8fa'

        exposure = self.create_exposure()
        print(exposure)

        policy = {
            "policyholderLocator": policyholder_locator,
            "productName": 'ビアガーデン経営者向け天候パラメトリック保険',
            "exposures": [exposure]
        }

        response = session.post('https://api.sandbox.socotra.com/policy',
                                json=policy)

        response1_json = response.json()
        GetInsuranceForm.policyLocator = response1_json['characteristics'][0]['policyLocator']



        print(GetInsuranceForm.policyLocator)
"""
        #Policy Issue
        response2 = session.post(
            'https://api.sandbox.socotra.com/policy/' + policyLocator + '/issue',
            )
        response2_json = response.json()
"""


class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()

