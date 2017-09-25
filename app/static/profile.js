$(document).ready(function() {

    // Initiate collapsible module
    $('.collapsible').collapsible();

    // Delete list
    $('.delete-list').click(function() {
      var $list = $(this).closest('div.card');
      var listid = $list.find('p').attr('id');
      if (confirm('Are You Sure?') == true) {
          $.ajax({
          url: '/deletelist/' + listid,
          data: $('.delete-list-form').serialize(),
          type: 'POST',
          success: function(data) {
            console.log(data);
            $list.remove();
          },
          error: function(error) {
            console.log(error);
            alert('Sorry, something went wrong.');
          }
          }); 
      } else {
          return false;
      };
    })


    // Add list 
    $(".add-btn").click(function() {
        $("#addlist-modal").addClass("is-active");
    });
      
    $("#newList-btn").click(function() {
        var newlist_name = $("#newList").val();
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
    
    $("#close-addlist-btn").click(function() {
        $("#addlist-modal").removeClass("is-active");
      });


    // Edit List Name
    $('.edit-list').click(function() {
      $('#editlist-modal').addClass("is-active");
      var listID = $(this).parentsUntil('div.card.a-list').find('p').attr('id');
      $("#rename-btn").data('listID', listID);
    });

    $('#rename-btn').click(function() {
        var listID = $(this).data('listID');
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

    $("#close-editlist-btn").click(function() {
      $("#editlist-modal").removeClass("is-active");
    });
    

    //  Edit item
    $('.edit-item').click(function() {
      var itemID = $(this).closest('li').attr('id');
      $('#edititem-modal').addClass('is-active'); 
      $('#rename-item-btn').data('itemid', itemID);
    });

    $('#rename-item-btn').click(function() {
      var itemID = $(this).data('itemid');
      $.ajax({
        url: '/renameitem/' + itemID,
        data: $('.rename-item-form').serialize(),
        type: 'POST',
        success: function(data) {
          console.log(data)
        },
        error: function(error) {
          console.log(error)
        }
      })
    });

    $("#close-edititem-btn").click(function() {
      $("#edititem-modal").removeClass("is-active");
    });


    // Delete Item
    $('.delete-item').click(function() {
      var $item = $(this).closest('li');
      var itemid = $item.attr('id');
      if (confirm('Are You Sure?') == true) {
          $.ajax({
          url: '/deleteitem/' + itemid,
          data: $('.delete-item-form').serialize(),
          type: 'POST',
          success: function(data) {
            console.log(data);
            $item.remove();
          },
          error: function(error) {
            console.log(error);
            alert('Sorry, something went wrong.');
          }
        });
      } else {
          return false;
      };
      
    });


    // Add Item
    $('.add-item').click(function() {
      $("#additem-modal").addClass("is-active");
      var chosenlistID = $(this).closest('div.card.a-list').find('p').attr('id');
      $("#add-item-btn").data('listId', chosenlistID);
    });

    $('#add-item-btn').click(function() {
      var chosenlistID = $(this).data('listId');
      $.ajax({
        url: '/additem/' + chosenlistID,
        data: $('.add-item-form').serialize(),
        type: 'POST',
        success: function(data) {
          console.log(data)
        },
        error: function(error) {
          console.log(error)
        }
      })
    });

    $("#close-additem-btn").click(function() {
      $("#additem-modal").removeClass("is-active");
    });


    // Change Status
    $('.change-status').click(function() {
      $('#changestatus-modal').addClass("is-active");
      var itemid = $(this).closest('li').attr('id');
      $("#change-status-btn").data('itemid', itemid);
    });

    $('#change-status-btn').click(function() {
      var itemid = $(this).data('itemid');
      $.ajax({
        url: '/changestatus/' + itemid,
        data: $('.change-status-form').serialize(),
        type: 'POST',
        success: function(data) {
          console.log(data)
        },
        error: function(error) {
          console.log(error)
        }
      })
    });

    $("#close-cs-btn").click(function() {
      $("#changestatus-modal").removeClass("is-active");
    });


    // Hover open functions
    $('.item').hover(function() {
      $(this).find('.item-functions').show();
    }, function() {
      $(this).find('.item-functions').hide();
    });

    // Hover open archived items
    $('.archived-pointer').hover(function() {
      $(this).find('.archived-items').show();
    }, function() {
      $(this).find('.archived-items').hide();
    });

  });
  
