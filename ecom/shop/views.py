from django.http import HttpResponse
from django.shortcuts import render
from .models import Product , Contact,orders
from math import ceil
# Create your views here.

# def index(request):
#     product = Product.objects.all()
#     print(product)
#     n = len(product)
#     nslides = n //4 + ceil((n/4) -(n//4))

#     # params =  {'no_of_slide':nslides,'range':range(1,nslides),'product':product}
#     allProds = [[product,range(1,nslides), nslides],[product,range(1,nslides),nslides]]
#     params = {'allProds':allProds}
#     return render(request,"shop/index.html",params)
#     #return HttpResponse(" index shop")

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
    # not requeired but good pratice to avoid error
    if request.method =="POST":
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        msg = request.POST.get("message")
        contact =Contact(name=name,email=email,desc=msg)
        contact.save()
        
    return render(request,"shop/contact.html")
    

def tracker(request):
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
        items_json= request.POST.get('itemsJson')
        name = request.POST.get("name")
        email = request.POST.get("email")
        address1 = request.Post.get("address1")
        address2 = request.Post.get("address2")
        address = address1 + " " +address2
        city = request.Post.get("city")
        state = request.Post.get("state")
        zip_code = request.Post.get("zip_code")
        phone = request.Post.get("phone")
        
        #ord =orders(items_json= items_json,name=name,email=email,phone=phone,address=address,city=city,sate=state,zip_code=zip_code)
        #ord.save()
    return render(request,"shop/checkout.html")
  
