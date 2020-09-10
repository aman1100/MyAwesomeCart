from math import ceil

from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Order,orderUpdate
import json

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

def search(request):

    return HttpResponse('search')

def productview(request,myid):
    product = Product.objects.filter(id = myid)
    print (product)
    return render(request,'shop/productview.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','')+ " " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        order = Order(items_json=item_json,name=name,phone=phone,email=email,address=address ,city =city ,state= state ,zip_code =zip_code)
        order.save()
        thank =True
        update = orderUpdate(order_id = order.order_id , update_desc ='The order has been placed')
        update.save()
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')

