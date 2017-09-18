$(function() {
	console.log('hi again');

	function render_lists(lists) {
		$('#lists').text('');
		for(var i = 0; i < lists.length; i++){
			var list_clone = $('.list').clone()
			list_clone.children('.name').text(lists[i].name)
			list_clone.children('.id').text(lists[i].id)
			list_clone.attr('id', 'list_' + lists[i].id)
			$('#lists').append(list_clone)
		}
	}
	function get_lists() {
		$.ajax({
			url: "/lists", 
			type:'GET', 
			success: function(result){
        		render_lists(result)
    		}
    	});
	};
	get_lists()

}) 