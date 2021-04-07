from . import forms

def form_order_work(request):
    return {
        'form_order_work': forms.OrderWorkForm
    }
