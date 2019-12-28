$(function(){
	$('#btn1').click(function(){

		$.ajax({
			url: '/xdxd',
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});