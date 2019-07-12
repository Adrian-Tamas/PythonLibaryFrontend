 jQuery(document).ready(function($) {

    // table
    $(".clickable-row").click(function() {
    if ($(this).hasClass("table-primary")) {
        $(this).removeClass("table-primary");
        $("#edit").removeData();
        $("#delete").removeData();
        $("#edit").attr("disabled", true);
        $("#delete").attr("disabled", true);
    } else {
        $(this).addClass("table-primary");
        $(".clickable-row").not($(this)).removeClass('table-primary');
        $("#edit").data("id", $(this).data("id"));
        $("#edit").attr("disabled", false);
        $("#delete").attr("disabled", false );
        $("#delete").data("id", $(this).data("id"));
    }
    });

    $(".clickable-reservation-row").click(function() {
    if ($(this).hasClass("table-primary")) {
        $(this).removeClass("table-primary");
        $("#edit-reservation").removeData();
        $("#edit-reservation").attr("disabled", true);
        $("#delete-reservation").attr("disabled", true);
    } else {
        $(this).addClass("table-primary");
        $(".clickable-reservation-row").not($(this)).removeClass('table-primary');
        $("#edit-reservation").data("userid", $(this).data("userid"));
        $("#edit-reservation").data("bookid", $(this).data("bookid"));
        $("#edit-reservation").attr("disabled", false);
        $("#delete-reservation").attr("disabled", false );
    }
    });

    // control buttons
    $("#edit").click(function() {
        var id = $(this).data("id")
        window.location.href = window.location.href + `/${id}`
    });

    $("#edit-reservation").click(function() {
        var userid = $(this).data("userid")
        var bookid = $(this).data("bookid")
        window.location.href = `/reservations/user/${userid}/book/${bookid}`
    });

    //delete model
    $("#modalCancelButton").click(function(event) {
        var id = $(this).data("id")
        $(".clickable-row").removeClass('table-primary');

        $("#edit").attr("disabled", true);
        $("#delete").attr("disabled", true);
    });

    $("#modelDelButton").click(function(event) {
        $(".clickable-row").removeClass('table-primary');

        $("#edit").attr("disabled", true);
        $("#delete").attr("disabled", true);
    });


    $(document).on('show.bs.modal', '#deleteModal', function (event) {
      var button = $(event.relatedTarget);// Button that triggered the modal
      var id = button.data('id');
      var page = button.data("page");
      var modal = $(this);
      var content = `Are you sure you want to delete the selected ${page}?`
      $('#deleteModalTitle').text("Delete " + page);
      $('#deleteMessage').text(content);
      var location = window.location.href +`/delete/${id}`
      $("#submitDelete").attr("action", location)
    });


    // search
    $(function () {
        $('#table').searchable({
            searchField: '#searchField',
            striped: true,
            oddRow: { 'background-color': '#f5f5f5' },
            evenRow: { 'background-color': '#fff' },
            searchType: 'fuzzy'
        });
    });
});