(function($) {
    $(function() {
        $(".button-collapse").sideNav();
        $(".parallax").parallax();
    }); // end of document ready
})(jQuery); // end of jQuery name space

$(".btn-concentration-name").on("click", function() {
  concentration_name = $(this).text();
  $("#concentration-name").val(concentration_name);
  $("#select-concentration").submit();

})

$("#btn-add-course").on("click", function() {
  $("#add-course").submit();

})

$(".btn-add-rating").on("click", function() {
  $(this).parent().parent().parent().submit();

})



















$("#btn-add-review").on("click", function() {
  $("#add-review").submit();
>>>>>>> 7896be372b4282c73ba10a46c7d6b39621683eba

})
