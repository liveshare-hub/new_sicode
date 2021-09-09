var numberOfItems = $("#loop .text-center").length;
var limitPerPage = 5;

$("#loop .text-center:gt(" + (limitPerPage - 1) + ")").hide();

var totalPages = Math.ceil(numberOfItems / limitPerPage);
$(".pagination.pagination-sm").append("<li class='page-item current-page active'><a class='page-link' href='javascript:void(0)'>" + 1 + "</a></li>");

for (var i = 2; i <= totalPages; i++){
    $(".pagination.pagination-sm").append("<li class='page-item current-page'><a class='page-link' href='javascript:void(0)'>" + i + "</a></li>");
}

$(".pagination.pagination-sm").append("<li class='page-item'><a class='page-link' href='javascript:void(0)'><span>Next <i class='fas fa-angle-right'></i></span></a></li>");

$(".pagination li.current-page").click(function(){
    if ($(this).hasClass("active")) {
        return false;
    } else {
        var curr_page = $(this).index();
        $(".pagination li").removeClass("active");
        $(this).addClass("active");
        $("#loop .text-center").hide();

        var grandTotal = limitPerPage * curr_page;
        
        for(var i = grandTotal - limitPerPage; i < grandTotal; i++){
            $("#loop .text-center:eq(" + i + ")").show();
        }

    }



    
})