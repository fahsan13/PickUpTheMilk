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
	query = $(this).val();
	$.get('/suggest_add_item/', {suggestion: query}, function(data){
		$('#Items').html(data);
	});
});

$(document).on("click", '#add_to_list', function(){
	alert("A button was clicked."); 
	var this_item;
	this_item = $(this).attr("data-itemtoadd");
	$.get('/item_needs_bought/', {item_adding: this_item}, function(data){
		$('#something').html(data);
			$('#add_to_list').hide();
	});
});
