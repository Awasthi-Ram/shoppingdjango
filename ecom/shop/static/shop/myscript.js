// find out the card from the card iteam from local storage
if (localStorage.getItem("cart") == null) {
  var cart = {};
} else {
  cart = JSON.parse(localStorage.getItem("cart"));

  updateCart(cart);
}

// $(".cart").click(function () {
  $('.divpr').on('click','button.cart',function(){
  var idstr = this.id.toString();
  console.log(idstr);
  if (cart[idstr] != undefined) {
    cart[idstr][0] = cart[idstr][0] + 1;
  } else {
    qty = 1;
    name =document.getElementById('name'+idstr).innerHTML;

    price =document.getElementById('price'+idstr).innerHTML;
    
    
    cart[idstr] = [qty,name,parseInt(price)];
  }
  
  
  updateCart(cart);
});
//add popover to cart
$("#popcart").popover();

updatepopover(cart);

function updatepopover(cart) {
  console.log("pop over");
  var popstr = "";

  popstr =
    popstr +
    "<h5> cart for your iteams in my shopping cart </h5><div class ='mx-2 my-2'>";
  var i = 1;
  for (var iteam in cart) {
    popstr = popstr + "<b>" + i + "  </b>. ";
    popstr =
      popstr +
      document.getElementById("name" + iteam).innerHTML.slice(0, 19) +
      "..." +
      " qty: " +
      cart[iteam][0] +
      "<br>";
    i = i + 1;
  }
 
  popstr =  popstr + "</div> <a href='/shop/checkout'><button class='btn btn-primary' id='checkout'>Checkout</button></a> <button class='btn btn-primary' id='clearcart' onclick='clearcart()'>Clear cart</button> ";
  document.getElementById("popcart").setAttribute("data-content", popstr);
  $("#popcart").popover("show");
}

function updateCart(cart) {
  var sum = 0;
  for (let iteam in cart) {
    sum = sum + cart[iteam][0];
    let k = iteam;
    document.getElementById("div" + k).innerHTML =
      "<button id='minus" +
      k +
      "' class='btn btn-primary minus'>-</button><span id='val" +
      k +
      "'>" +
      cart[iteam][0] +
      "</span> <button id='plus" +
      k +
      "' class='btn btn-primary plus'>+</button>";
  }
  localStorage.setItem("cart", JSON.stringify(cart));
  document.getElementById("cartno").innerHTML = sum;
  console.log(cart);
  updatepopover(cart);
}

function clearcart(){
  cart = JSON.parse(localStorage.getItem('cart'));
  for(let iteam in cart){
    document.getElementById('div'+iteam).innerHTML = '<button id="'+ iteam +'"  class="btn btn-primary cart">add to cart</button>';
  }
  localStorage.clear();
  cart = {};
  updateCart(cart);
}
//if plus and minus button is click

$(".divpr").on("click", "button.minus", function () {
  console.log("minus clicked");

  a = this.id.slice(7);
  cart["pr" + a][0] = cart["pr" + a][0] - 1;
  cart["pr" + a][0] = Math.max(0, cart["pr" + a][0]);

  document.getElementById("valpr" + a).innerHTML = cart["pr" + a][0];
  updateCart(cart);
  console.log(a);
});

$(".divpr").on("click", "button.plus", function () {
  console.log("plus clicked");

  a = this.id.slice(6);
  cart["pr" + a][0] = cart["pr" + a][0] + 1;
  document.getElementById("valpr" + a).innerHTML = cart["pr" + a][0];
  updateCart(cart);
  console.log(a);
});
