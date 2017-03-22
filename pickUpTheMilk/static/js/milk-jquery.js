
$(document).ready(function () {

});

$('#settle_balance').click(function(){
	alert("The settle button was clicked."); 
	var thisGroup;
	thisGroup = $(this).attr("groupname");
	$.get('MILK/settle-up/', {something: groupname}, function(data){
		$('#something').html(data);
			$('#likes').hide();
	});
});

