/**
 * Created by David on 11/03/2017.
 */
// $('#list').

$('#settle_balance').click(function(){
	var thisGroup;
	alert= "fun"
	thisGroup = $(this).attr("data-groupname");
	$.get('/resolvebalances/', {group_name: thisGroup}, function(data){
		$('#balances').html(data);
			$('#settle_balance').hide();
	});
});