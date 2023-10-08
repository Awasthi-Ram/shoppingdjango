from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Product , Contact,orders,orderupdate
from math import ceil


from django.views.decorators.csrf import csrf_exempt
import json


import json

import razorpay
from django.conf import settings






MERCHANT_KEY = 'bKMfNxPPf_QdZppa'

def searchMatch(query,item):
    ''' return true when query matches the iteam '''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {iteam['category'] for iteam in catprods}

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query.lower(),item)]
        for item in prod:
            if len(item.desc) > 30:
                print(len(item.desc))
                item.desc = item.desc[:30] + '...'
        n = len(prod)
        nslides = n //4 + ceil((n/4) -(n//4))
        if n != 0:   
            allProds.append([prod ,range(1,nslides),nslides])  
      
    params = {'allProds':allProds,"msg":""}
    if len(allProds) == 0 or len(query)<3:
        params = {'msg':" please make sure to enter relavent search queary"}
    print(len(allProds))
    
    return render(request,"shop/search.html",params)
    
def index(request):

    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {iteam['category'] for iteam in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        for item in prod:
            if len(item.desc) > 30:
                print(len(item.desc))
                item.desc = item.desc[:30] + '...'
        n = len(prod)
        nslides = n //4 + ceil((n/4) -(n//4))
        allProds.append([prod ,range(1,nslides),nslides])  
      
    params = {'allProds':allProds}
    
    return render(request,"shop/index.html",params)
    #return HttpResponse(" index shop")

def about(request):
    return render(request,"shop/about.html")
    # return HttpResponse("i am about")

def contact(request):
    thank = False
    # not requeired but good pratice to avoid error
    if request.method =="POST":
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        msg = request.POST.get("message")
        contact =Contact(name=name,email=email,desc=msg)
        contact.save()
        thank =True
        
    return render(request,"shop/contact.html",{'thank':thank})
    

def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid',"")
        email = request.POST.get('email','')
        #return (HttpResponse(orderid + " "+ email))
        try:
            order = orders.objects.filter(order_id = orderid ,email = email)
            if(len(order) > 0):
                update = orderupdate.objects.filter(order_id = orderid)
                updates = []
                for iteam in update:
                    updates.append({'text': iteam.update_desc,'time':iteam.timestamp})
                    # responce = json.dumps([updates,order[0].iteams_json] ,default=str)
                    responce = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].iteams_json} ,default=str)
                return HttpResponse(responce)
            else:
                return HttpResponse(' {"staus":"noitem"} ')
                
        except Exception as e:
            return HttpResponse(' {"staus":"error"}')
    return render(request,"shop/tracker.html")
    

def productview(request,id):
    # featch the product using the id
    product = Product.objects.get(id=id)
    #category, desc, id, image, price, product_name, pub_date, subcategory
    print(product)
    print(product)
    return render(request,"shop/productview.html",{'product':product})


@csrf_exempt
def checkout(request):
    if request.method =="POST":
        items_json= request.POST.get('iteamjson')
        name = request.POST.get("name")
        amount = request.POST.get("amount","")
        email = request.POST.get("email")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        address = address1 + " " +address2
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        ord =orders(iteams_json= items_json,name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code,amount=amount)
        
        print(ord)
        return payment(request,ord,amount)

        
       
    print("no post")
    return render(request, 'shop/checkout.html')


            
@csrf_exempt
def payment(request,ord,amount):
    
        print("i am in post")
        try :    
            client = razorpay.Client(auth =('rzp_test_AV8KfcQsdHfG66','8tpvUnQGLA13wI3udYRa2mMt'))
            
            payment_data = {
                'amount': int(amount)* 100,
                'currency': 'INR',
                'payment_capture': '1'
                }
            client.set_app_details({"title" : "Django", "version" : "4.2.4"})
            payment = client.order.create(data=payment_data)
            print(payment)
            ord.payment_id = payment['id']
            ord.save()
            print(payment['id']) 
            myord = orders.objects.filter(order_id = ord.order_id)
            total_amount = myord.values('amount')
            final_amount = total_amount[0]['amount']

            print(type(final_amount))
            
            context = {'ord':ord,'payment':payment}
            print("**********")
            print(context)
            print("*****************")
            return render(request, 'shop/payment.html', {'context':context})
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
    

def success(request):
    order_ida = request.GET.get('order_id')
    print(order_ida)
    ord = orders.objects.get(payment_id = order_ida)
    ord.is_paid = True
    update = orderupdate(order_id = ord.order_id,update_desc = " this order has been created",order_status = True)
    update.save()
    ord.save()
    payment = True
    #return HttpResponse('payment Success')
    return render(request, 'shop/checkout.html',{'ord':ord,"paymentstatus":payment})

