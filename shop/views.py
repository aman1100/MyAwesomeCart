from math import ceil

#from django.utils.decorators import method_decorator ## import this to use method decorator at csrf methd below(handlerequest)
from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Order,orderUpdate
import json
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum

MERCHANT_KEY = 'J6hCMxWH@3_Qyt9C'

# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods} #categories
    for cat in cats: #cat = category
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)
def searchMatch(query,item):
    ''':return true only  if qury matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}  # categories
    for cat in cats:  # cat = category
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds,'msg':"" }
    if len(allProds) == 0 or len(query)<4:
        params = {'msg':'Item not found please enter valid search query'}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request,'shop/about.html')

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,phone=phone,email=email,desc=desc)
        contact.save()
        return render(request, 'shop/contactus.html', {'contact': contact})
    return render(request,'shop/contactus.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = orderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')



def productview(request,myid):
    product = Product.objects.filter(id = myid)
    print (product)
    return render(request,'shop/productview.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','')+ " " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        order = Order(amount=amount,items_json=item_json,name=name,phone=phone,email=email,address=address ,city =city ,state= state ,zip_code =zip_code)
        order.save()
        thank =True
        update = orderUpdate(order_id = order.order_id , update_desc ='The order has been placed')
        update.save()
        id = order.order_id
        #return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    #return render(request, 'shop/checkout.html')
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

            'MID': 'jsuOET59271788796700',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request,'shop/checkout.html')

#@method_decorator(csrf_exempt, name='dispatch') use this at main server to bypass csrf token
@csrf_exempt
def handlerequest(request):
    #paytm will send you post request here
    form = request.POST
    response_dict ={}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify =Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('ORDER SUCCESFUL')
        else:
            print("ORDER WAS NOT SUCCESFUL BECAUSE" + response_dict['RESPMSG'])

    return render(request,'shop/paymentstatus.html',{'response':response_dict})

