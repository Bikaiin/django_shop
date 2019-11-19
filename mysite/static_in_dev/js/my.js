var domain = "http://127.0.0.1:8000";
$(document).ready(function(){
    var scrValue = $('img.bigimg').attr('src');
    scrValue = $('#gallery a').attr('href')
    $('#gallery a').on('click',function(e){
        e.preventDefault();
        scrValue = $(this).attr('href');
        $('img.bigimg').attr('src', scrValue)
    })

    $('.add_to_cart').on('click',function(e){
        product_slug = $(this).attr('data-slug')
        e.preventDefault();
        var settings = {
		    url: domain + '/add_to_cart',
		    method: "GET",
		    dataType: "json",
		    contentType: "application/json",
		    data: {product_slug:product_slug }
        }
        $.ajax(settings).done(function(response){
            $("#cart_count").html(response.cart_total)
        })
    })

    $('.cart-item-qty').bind('keyup mouseup',function(e){
        qty = $(this).val()
        item_id = $(this).attr('data-id')
        var settings = {
		    url: domain + '/change_item_qty',
		    method: "GET",
		    dataType: "json",
		    contentType: "application/json",
		    data: {
		        qty:qty,
		        item_id:item_id
		    }
        }
        $.ajax(settings).done(function(response){
            $('#cart_total').html('<strong>' + response.cart_total_price + ' руб.'+'</strong>')
            $('#cart-item-total-'+item_id).html(response.item_total + ' руб.')

        })

    })
    $('#id_date_month').addClass('col-lg-4')
    $('#id_date_day').addClass('col-lg-4')
    $('#id_date_year').addClass('col-lg-4   ')
    $('#id_date_year').css('display', 'inline')
    $('#id_date_day').css('display', 'inline')
    $('#id_date_month').css('display', 'inline')

    $('#div_id_address').addClass('d-none')
    $('#id_buying_type').on('click', function(){
        buying_type = $(this).val()
        console.log(buying_type)
        if (buying_type == 'delivery'){
            $('#div_id_address').removeClass('d-none')
        }
        else{
            $('#div_id_address').addClass('d-none')
        }
    })

    $('.remove_from_cart').on('click',function(e){
        product_slug = $(this).attr('data-slug')
        e.preventDefault();
        item_product_id = $(this).attr('data-id')
        var settings = {
		    url: domain + '/remove_from_cart',
		    method: "GET",
		    dataType: "json",
		    contentType: "application/json",
		    data: {product_slug:product_slug }
        }
        $.ajax(settings).done(function(response){
            $("#cart_count").html(response.cart_total)
            $('.cart-item-'+item_product_id).css('display', 'none')
            $('#cart_total').html('<strong>' + response.cart_total_price + ' руб.' +'</strong>')

            if(parseInt(response.cart_total)==0){
                $('.my_cart').addClass("d-none")
                $('.cart_empty').removeClass("d-none")

            }
        })
    })


})

