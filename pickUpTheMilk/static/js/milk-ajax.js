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
