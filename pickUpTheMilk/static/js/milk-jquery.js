// Don't process any JQuery until the page is loaded.
$(document).ready(function () {

	// Hovertext for various sections of the website. Each line refers to a div or button ID.
	$("#addItemButton").attr('title', 'Use this button to add a new item to your group\'s shopping list. Any newly added item will be added to your \'Items To Pick Up\' list by default.');
	$("#pickUpItemButton").attr('title', 'Use this button to let your group know that an existing item on your shopping list needs to be bought.');
	$("#recordPurchaseButton").attr('title', 'Use this button to record the purchase of an item on your \'Items To Pick Up\' list. Any purchase will be reflected on your indiviual spending balance.');
	$("#completelist").attr('title', 'This list is a history of all the items that your group has added.');
	$("#pickuplist").attr('title', 'This list contains all the items that your group needs to buy.');
	$("#additemdiv").attr('title', 'Add a new item to your communal list. See your full shopping list below.');
	$("#profilepicdiv").attr('title', 'Update your profile picture - supports gifs!');
	$("#memberdiv").attr('title', 'Click on the links to visit your groups members\' profiles.');
	$("#average_balances").attr('title', 'Get a snapshot of current group spending.');
	$("#settle_balance").attr('title', 'ADMIN ONLY - reset balances. Cannot be undone!');
	$("#initial").attr('title', 'Summary of spending since your group last settled up.');
});
