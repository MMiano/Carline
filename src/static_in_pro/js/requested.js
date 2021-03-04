


$(document).ready(function(){
	
	
$('button.req').click(function(){
	
	var product_id;
	productid = $(this).attr("data-id");
	control = $(this);

 $.get('/request/', {'product_id': productid}, function(data){
	  	
	    if (data.has_error){
	        	
	       	console.log("Requested by: "+ data.requested_by);
	       	alert("Requested by: "+ data.requested_by);

	        }
	        else if(data.withdraw_request){
	        	control.fadeOut(200, function(){
	        		control.removeClass("requested").fadeIn(200);
	        		control.text("Request");

	        	});
	        	
	        }
	        
	        else if(data.make_request){	  
	        	control.fadeOut(200, function(){
	        		control.addClass("requested").fadeIn(200);
	        		control.text("Requested / Withdraw");
	        	});      	
	        	

	        }


	  }

 		);
 	});



});


$(document).ready(function(){
$('a.confirm-request').click(function(){

	var productid;

	productid = $(this).attr("data-id");
	
	$.get('/owned_parts/confirm_request/', {'product_id': productid}, function(data){


			$('#js-transaction-form').html(data.html_form)
			$('#js-product-title').html(data.title)
			$('#js-product-description').html(data.description)
			$('#js-recepient-names').html(data.recepient_names)
			$('#js-recepient-email').html(data.recepient_email)
			$('#js-recepient-username').html(data.recepient_username)

			$('#div_id_is_available').css('display','none');
			$('#div_id_is_active').css('display','none');
	

			
		

	});


});

});

$(document).ready(function(){
$('a.revoke-request').click(function(){

	var productid;

	productid = $(this).attr("data-id");
	
	$.get('/owned_parts/revoke_request/', {'product_id': productid}, function(data){


			$('#js-revoke-form').html(data.html_form)
			$('#revoke-js-product-title').html(data.title)
			$('#revoke-js-product-description').html(data.description)
			$('#revoke-js-recepient-names').html(data.recepient_names)
			$('#revoke-js-recepient-email').html(data.recepient_email)
			$('#revoke-js-recepient-username').html(data.recepient_username)

			$('#div_id_is_available').css('display','none');
			$('#div_id_is_active').css('display','none');
	

			
		

	});


});

});




$('#js-transaction-form').on('submit', '#js-confirm-request-form', function(){

	var form = $(this);

	$.ajax({

		headers: { "X-CSRFToken": $.cookie("csrftoken") },
		url: form.attr('action'),
		type: form.attr('method'),
		data: form.serialize,
		dataType: 'json',

		success: function(data){

			if(data.form_is_valid){
				$('#approve-modal').modal('hide');
				window.location.reload();
			}
			else{
				$('#js-transaction-form').html(data.html_form);
			}
		}



	});

	return false;
});

$('#js-revoke-form').on('submit', '#js-revoke-request-form', function(){

	var form = $(this);

	$.ajax({

		headers: { "X-CSRFToken": $.cookie("csrftoken") },
		url: form.attr('action'),
		type: form.attr('method'),
		data: form.serialize,
		dataType: 'json',

		success: function(data){

			if(data.form_is_valid){
				$('#revoke-modal').modal('hide');
				window.location.reload();
			}
			else{
				$('#js-revoke-form').html(data.html_form);
			}
		}



	});

	return false;
});

