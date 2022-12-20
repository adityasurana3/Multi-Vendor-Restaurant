let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in',]},
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
        if(status==google.maps.geocodersStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);
        }
    });
    
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
                }
            }
        })
        $('.item_qty').each(function(){
            var the_id = $(this).attr('id')
            var qty = $(this).attr('data-qty')
            $('#'+the_id).html(qty)
        })
    })

});


