$(document).ready(function() {
    $('#delete-list').click(function() {
      $('#delete-form').submit();
    });
    
    $(".add-btn").click(function() {
        $("#addlist-modal").addClass("is-active");
    });
      
    $("#newList-btn").click(function() {
        // var newlist_name = $("#newList").val();
        $.ajax({
          url: '/newlist',
          data: $('.new-list-form').serialize(),
          type: 'POST',
          success: function(data) {
            console.log(data);
          },
          error: function(error) {
            console.log(error);
          }
        });
      });
      
    $('.edit-list').click(function() {
      $('#editlist-modal').addClass("is-active");
      var listID = $(this).attr('id');
      $('#rename-btn').click(function() {
        var list_name = $('#inputListName').val();
        $.ajax({
          url: '/renamelist/' + listID,
          data: $('.rename-form').serialize(),
          type: 'POST',
          success: function(data) {
            console.log(data)
          },
          error: function(error) {
            console.log(error);
          }
        });
        setInterval(function(){
           $("#l" + listID).load('profile.html .a-list');
        }, 1500)
      });
      
      $("#close-addlist-btn").click(function() {
        $("#addlist-modal").removeClass("is-active");
      });
      
      $("#close-editlist-btn").click(function() {
        $("#editlist-modal").removeClass("is-active");
      });
      
      

    });
  });
  

      
