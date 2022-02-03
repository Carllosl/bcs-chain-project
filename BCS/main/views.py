from django.shortcuts import render
from .models import Transaction
from .rpc import new_trans

def index(request):
    transactions = Transaction.objects.order_by('-id')
    if request.method == 'POST':
        trans = Transaction(trans_id = new_trans(), trans_description = 'null')
        trans.save()
    return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'transactions': transactions})
