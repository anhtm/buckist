$(document).ready(function() {

    //  Delete list func
    $('#delete-list').click(function() {
      $('#delete-form').submit();
    });
    

    // Add list func
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


    //  Edit list func
    $('.edit-list').click(function() {
      $('#editlist-modal').addClass("is-active");
      var listID = $(this).parentsUntil('div.card.a-list').find('p').attr('id');
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
      
      $("#close-editlist-btn").click(function() {
        $("#editlist-modal").removeClass("is-active");
      });

      
      //  Edit item func
      $('.edit-item').click(function() {
        var itemID = $(this).parent().attr('id');
        $('#edititem-box').removeClass('hidden');
        $('#edititem-modal').addClass('is-active');
        $('#rename-item-btn').click(function() {
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
      })

      });

      $("#close-edititem-btn").click(function() {
        $("#edititem-modal").removeClass("is-active");
      });


      // Try Hidden class

      // $('#edit-item38').on('click', function() {
      //   $('#edititem-box').removeClass('hidden');
      //   var itemID = $(this).parent().attr('id');
      //   $('#rename-item-btn').click(function() {
      //     $.ajax({
      //     url: '/renameitem/' + itemID,
      //     data: $('.rename-item-form').serialize(),
      //     type: 'POST',
      //     success: function(data) {
      //       console.log(data)
      //     },
      //     error: function(error) {
      //       console.log(error)
      //     }
      //   })
      // })
      // });

      // $('#turn-on-edit').click(function() {
      //   $('#edititem-box').removeClass('hidden');
      //   $('#additem-box').removeClass('hidden');
      // });

      
      // Add Item Func
      $("#close-additem-btn").click(function() {
        $("#additem-modal").removeClass("is-active");
      });

      $('.add-item').click(function() {
        $("#additem-modal").addClass("is-active");
        var chosenlistID = $(this).parentsUntil('div.card.a-list').siblings().children().attr('id');
        $('#add-item-btn').click(function() {
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
        })
      });


      // Delete Item Func
      $('.delete-item').click(function() {
        var itemid = $(this).parent().attr('id');

       })

    });
  });
  

      
