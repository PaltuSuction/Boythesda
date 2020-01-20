from _sha256 import sha256

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from robokassa.forms import RobokassaForm

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, game=item['game'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            #return render(request, 'created.html', {'order': order})
            #return redirect(pay_with_robokassa, order_id = order.id)
            return (pay_with_robokassa(request, order.id))

    if request.user.is_authenticated:
        form = OrderCreateForm(initial={'first_name' : request.user.first_name,
                                        'last_name' : request.user.last_name,
                                        'email':request.user.userprofile.user_email})
    else:
        form = OrderCreateForm()
    return render(request, 'create.html', {'cart': cart, 'form': form})


@login_required
def pay_with_robokassa(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    #Получение id пользователя
    user = request.user.id
    #Данные магазина
    mrh_login = "Test1999"
    mrh_pass1 = "password_1"
    inv_id  = user
    inv_desc  = order.first_name + "_" + order.last_name
    out_summ  = order.get_total_cost()
    #Формирование контрольной суммы
    result_string = "{}:{}:{}:{}".format(mrh_login, out_summ, inv_id, mrh_pass1)
    sign_hash = sha256(result_string.encode())
    crc = sign_hash.hexdigest().upper()
    #Указание тестового режима
    isTest = 1
    url = "https://auth.robokassa.ru/Merchant/Index.aspx?MrchLogin={}&OutSum={}&InvId={}&Desc={}&SignatureValue={}&IsTest={}/".format(mrh_login, out_summ, inv_id, inv_desc, crc, isTest)
    '''
    url_test = 'https://auth.robokassa.ru/Merchant/PaymentForm/FormMS.js?MerchantLogin={}&OutSum={}&InvoiceID={}&Description={}&SignatureValue={}&IsTest=1'.format(
        mrh_login, out_summ, inv_id, inv_desc, crc
    )
    '''
    if request.method == "POST":
        #Запись в таблицу пополнения
        return HttpResponseRedirect(url)
        #return render(request, 'created.html', context={'payment_form_url' : url_test})
    return render(request, 'created.html')


'''
@login_required
def pay_with_robokassa(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    form = RobokassaForm(initial={
               'OutSum': order.get_total_cost(),
               'InvId': order.id,
               'Desc': order.first_name + '_' + order.last_name,
               'Email': request.user.email,
               # 'IncCurrLabel': '',
               # 'Culture': 'ru'
           })

    return render(request, 'payment/pay_with_robokassa.html', {'form': form})

'''


