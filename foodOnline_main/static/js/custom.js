let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in','np']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({"address":address},function(results,status){
        if(status==google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);
        }
    });
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }
}
$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        console.log("Hello World")
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        data = {
            food_id:food_id,
        }
        console.log("data=>",data)
        $.ajax({
            type : 'GET',
            url:url,
            data:data,
            // Response from backend
            success : function(responce){
                if(responce.status=='login_requires'){
                    swal(responce.message,'','info').then(function(){
                        window.location = '/login'
                    })
                }else if (responce.status=='Failed'){
                    swal(responce.message,'','error')
                }else{
                console.log(responce)
                $('#cart-counter').html(responce.cart_counter['cart_count'])
                $('#qty-'+food_id).html(responce.qty)
                applyCartAmount(responce.cart_amount['subtotal'],responce.cart_amount['tax'],responce.cart_amount['grand_total'])
                }
            }
        })
    })
    // place the cart item quantity on load
    $('.item_qty').each(function () { 
         var the_id = $(this).attr('id')
         var qty = $(this).attr('data-qty')
         $('#'+the_id).html(qty);
    });

    // decrease cart    

    $('.decrease_cart').on('click',function(e){
        e.preventDefault()
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        cart_id = $(this).attr('id')
        data ={
            food_id:food_id
        }
        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success : function(responce){
                if(responce.status == 'login_required'){
                    swal(responce.message,'','info').then(function(){
                        window.location('/login')
                    })
                }else if (responce.status == 'Failed'){
                    swal(responce.message,'','error')
                }else{
                    $('#cart-counter').html(responce.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(responce.qty)
                    applyCartAmount(responce.cart_amount['subtotal'],responce.cart_amount['tax'],responce.cart_amount['grand_total'])
                    if (window.location.pathname == '/cart/'){
                        removeCartItem(responce.qty,cart_id);
                        checkEmptyCart();
                    }
                }
            }
        })
        $('.item_qty').each(function(){
            var the_id = $(this).attr('id')
            var qty = $(this).attr('data-qty')
            $('#'+the_id).html(qty)
        })
    })
    // Delete Cart
    $('.delete_cart').on('click',function(e){
        e.preventDefault()
        cart_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        $.ajax({
            type:'GET',
            url:url,
            success : function(responce){
                if (responce.status == 'Failed'){
                    swal(responce.message,'','error')
                }else{
                    $('#cart-counter').html(responce.cart_counter['cart_count'])
                    swal(responce.status,responce.message,"success")
                    applyCartAmount(responce.cart_amount['subtotal'],responce.cart_amount['tax'],responce.cart_amount['grand_total'])
                    removeCartItem(0,cart_id);
                    checkEmptyCart()
                }
            }
        })
    })
    // Remome the cartitem when the item is 0
    function removeCartItem(cartItemQty,cart_id){
        if (cartItemQty<=0){
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart-counter').innerHTML
        if (cart_counter == 0){
            document.getElementById('empty-cart').style.display = "block";
        }
    }

    // Apply cart amount
    function applyCartAmount(subtotal,tax,grand_total){
        if (window.location.pathname == '/cart/'){
            // Using JQuery
            
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
            
            // Using JavaScript
            // document.getElementById('subtotal').innerHTML = subtotal
            // document.getElementById('tax').innerHTML = tax
            // document.getElementById('total').innerHTML = grand_total
        }
    }
});
// API KEY -> AIzaSyA1F4R_QASLq4AyHv-eH46iny5ZK9VOUgM

