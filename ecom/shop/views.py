from django.http import HttpResponse
from django.shortcuts import render
from .models import Product , Contact,orders,orderupdate
from math import ceil

import json

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
                    responce = json.dumps([updates,order[0].iteams_json] ,default=str)
                return HttpResponse(responce)
            else:
                return HttpResponse(" {} ")
                
        except Exception as e:
            return HttpResponse(" {}")
    return render(request,"shop/tracker.html")
    
def search(request):
    return render(request,"shop/search.html")
    
def productview(request,id):
    # featch the product using the id
    product = Product.objects.get(id=id)
    #category, desc, id, image, price, product_name, pub_date, subcategory
    print(product)
    print(product)
    return render(request,"shop/productview.html",{'product':product})
    

def checkout(request):
    if request.method =="POST":
        items_json= request.POST.get('iteamjson')
        name = request.POST.get("name")
        email = request.POST.get("email")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        address = address1 + " " +address2
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        
        ord =orders(iteams_json= items_json,name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        #ord =orders(name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        ord.save()
        update = orderupdate(order_id = ord.order_id,update_desc = " this order has been created")
        update.save()
        thank =True
        id = ord.order_id
        return render(request,"shop/checkout.html",{'thank':thank,'id':id})
    return render(request,"shop/checkout.html")
  
