/**
 * Created by David on 11/03/2017.
 */
// $('#list').

$('#settle_balance').click(function(){
	var groupname;
	groupname = $(this).attr("data-groupname");
	$.get('/resolvebalances/', {group_name: groupname}, function(data){
		$('#balances').html(data);
			$('#settle_balance').hide();
	});
});