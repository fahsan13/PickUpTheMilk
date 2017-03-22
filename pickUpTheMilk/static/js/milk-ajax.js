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

// JQuery to search for a user to add to a group
$('#usersearch').keyup(function(){
	var query;
	var user_group;
	query = $(this).val();
	user_group = $(this).attr("data-groupname");
	$.get('/user_search/', {suggestion: query}, function(data){
		$('#Users').html(data);
	});
});

//
$(document).on("click", '#add_to_group', function(){
	var this_user;
	this_user = $(this).attr("data-usertoadd");
	alert(this_user + " has been added to your group!");
	$.get('/add_user/', {user_adding: this_user}, function(data){
		// Refresh div which contains 'items to pick up' list
		$('#add_to_group').hide();
		// Refresh modal window
		// 	$('#pickUp').reset();
		location.reload();
	});
});

$(document).on("click", '#add_to_list', function(){
	var this_item;
	this_item = $(this).attr("data-itemtoadd");
	alert(this_item + " has been added to your 'Items To Pick Up' list!");
	$.get('/item_needs_bought/', {item_adding: this_item}, function(data){
		// Refresh div which contains 'items to pick up' list
		$('#pickuplist').html(data);
		$('#add_to_list').hide();
		// Refresh modal window
		// 	$('#pickUp').reset();
		location.reload();
	});
});

$('#settle_balance').click(function(){
	var user_group;
	user_group = $(this).attr("data-groupname");
	var popup = confirm("Warning! This operation cannot be undone. Are you sure you wish to settlle balances for " + user_group + "?");

	if (popup==true) {
		$.get('/resolve_balances/', {current_group: user_group}, function(data){
			$('#settled_balances').html(data);
			$("#initial").replaceWith('');
			$("#averaged_balances").replaceWith('')
		});
	}
});

$('#average_balances').click(function(){
	alert("Clicking this button will return a snapshot of your group's current spending. Please note that only your group administrator can reset group balances.");
	var user_group;
	user_group = $(this).attr("data-groupname");
	$.get('/average_balances/', {current_group: user_group}, function(data){
		$('#averaged_balances').html(data);
	});
});
