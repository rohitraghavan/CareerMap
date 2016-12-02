//Initialize form
(function($) {
    $(function() {
        $(".button-collapse").sideNav();
        $(".parallax").parallax();
    });
})(jQuery);

//Submit Select Concentration form on Concentration button click
$(".btn-concentration-name").on("click", function() {
    concentration_name = $(this).text();
    $("#concentration-name").val(concentration_name);
    $("#select-concentration").submit();

})


//Submit Add Course form on Add Course button click
$("#btn-add-course").on("click", function() {
    $("#add-course").submit();

})

//Submit Add Rating form on Add Rating button click
$(".btn-add-rating").on("click", function() {
    $(this).parent().parent().parent().submit();

})

//Submit Reviews form on Add Reviews button click
$(".btn-reviews").on("click", function() {
    $(this).parent().submit();

})

//Submit Add Review form on Add Review button click
$("#btn-add-review").on("click", function() {
    $("#add-review").submit();

})

//Validates Add Review form
function validateAddReviewForm() {
    if ($("#review")[0].value === "") {
        alert("Please add a review.");
        return false;
    }
    return true;
}

//Validates Add Course form
function validateAddCourseForm() {
    if ($("#course_id")[0].value === "" || $("#course_name")[0].value === "" || $("#instructor")[0].value === "") {
        alert("Please fill in all fields.");
        return false;
    }
    return true;
}
