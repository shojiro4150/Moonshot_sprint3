import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm,GetInsuranceForm
from .import confirm
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "index.html"

class GetInsuranceView(generic.FormView):
    template_name = "get_insurance.html"
    form_class = GetInsuranceForm
    success_url = reverse_lazy('ec:confirm_insurance')

    def form_valid(self, form):
        form.send_socotra()
        messages.success(self.request, '登録完了しました。')
        return super().form_valid(form)

class ConfirmInsuranceView(generic.TemplateView):
    template_name = 'confirm_insurance.html'
  
    def get_context_data(self, **kwargs): # 追加
        found_policy = confirm.DetailConfirm()

        context = super().get_context_data(**kwargs)
        context['pol_no'] = found_policy[0]['locator']
        context['name'] = GetInsuranceForm.name
        context['email'] = GetInsuranceForm.email
        context['store_name'] = found_policy[0]['exposures'][0]['characteristics'][0]['fieldValues']["store_name"][0]
        context['price'] = found_policy[0]['characteristics'][0]["grossPremium"]
        context['paypay_url'] = found_policy[1]

        return context

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('ec:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
