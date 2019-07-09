 jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
    if ($(this).hasClass("table-primary")) {
        $(this).removeClass("table-primary");
        $("#edit").removeData();
        $("#edit").attr("disabled", true);
        $("#delete").attr("disabled", true);
    } else {
        $(this).addClass("table-primary");
        $(".clickable-row").not($(this)).removeClass('table-primary');
        $("#edit").data("id", $(this).data("id"));
        $("#edit").attr("disabled", false);
        $("#delete").attr("disabled", false );
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

    $("#edit").click(function() {
        var id = $(this).data("id")
        window.location.href = window.location.href + `/${id}`
    });

    $("#edit-reservation").click(function() {
        var userid = $(this).data("userid")
        var bookid = $(this).data("bookid")
        window.location.href = `/reservations/user/${userid}/book/${bookid}`
    });
});