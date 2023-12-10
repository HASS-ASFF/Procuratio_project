$(document).ready(function(){

// Add to cart
	$(document).on('click',".add-to-cart",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _productId=$(".product-id-"+_index).val();
		var _qty=$(".product-qty-"+_index).val();
		var _productImage=$(".product-image-"+_index).val();
		var _productTitle=$(".product-title-"+_index).val();
		var _productPrice=$(".product-price-"+_index).val();

		// Ajax
		$.ajax({
			url:'/add-to-cart',
			data:{
				'id':_productId,
				'qty':_qty,
				'image':_productImage,
				'price':_productPrice,
				'title':_productTitle
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
			}
		});
		// End

	});
	// End

	//
// Delete item from cart
	$(document).on('click','.delete-item',function(){

		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				setInterval('location.reload()', 50);
				_vm.attr('disabled',true);
			},
			success:function(res){
				//$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});


// Update item from cart
	$(document).on('click','.update-item',function(){

		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				setInterval('location.reload()', 50);
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").unblock();
			}
		});
		// End
	});

});

// Add to cart with fidelity code
$(document).on('click', ".fidelity-code", function () {
	var _vm=$(this);
	var _index=_vm.attr('data-fidelity');
	var _fidelityCode=$(".fidelity-code-"+_index).val();
	console.log(_fidelityCode);

    // Ajax
    $.ajax({
        url: '/fidelity-update',
        data: {
            'fidelity_code': _fidelityCode,
        },
        dataType: 'json',
        beforeSend:function(){
				setInterval('location.reload()', 50);
				_vm.attr('disabled',true);
		},
        success: function (res) {

			_vm.attr('disabled', false);
            $("#cartList").unblock();
        }
    });
    // End

});
// End
