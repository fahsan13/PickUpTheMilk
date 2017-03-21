/**
 * Created by David on 11/03/2017.
 */
// $('#list').

$('#suggestion').keyup(function(){
	var query;
	query = $(this).val();
	$.get('/suggest_item/', {suggestion: query}, function(data){
		$('#Items').html(data);
	});
});


$('#needsBoughtSuggestion').keyup(function(){
	var query;
	var user_group;
	query = $(this).val();
	user_group = $(this).attr("data-groupname");
	$.get('/suggest_add_item/', {suggestion: query}, function(data){
		$('#Items').html(data);
	});
});

$(document).on("click", '#add_to_list', function(){
	var this_item;
	this_item = $(this).attr("data-itemtoadd");
	alert(this_item + " has been added to your shopping list!");
	$.get('/item_needs_bought/', {item_adding: this_item}, function(data){
		$('#something').html(data);
		$('#add_to_list').hide();
	});
});

$('#settle_balance').click(function(){
	var user_group;
	user_group = $(this).attr("data-groupname");
	alert("Balances settled for " + user_group);
	$.get('/resolve_balances/', {current_group: user_group}, function(data){
		$('#settled_balances').html(data);
		$("#initial").replaceWith('')
	});
});

$('#average_balances').click(function(){
	alert("AVERAGE BALANCES NOW PLZ THANKS");
	var user_group;
	user_group = $(this).attr("data-groupname");
	$.get('/average_balances/', {current_group: user_group}, function(data){
		$('#averaged_balances').html(data);
	});
});
