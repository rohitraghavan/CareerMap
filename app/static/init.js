//Initialize form
(function($) {
    $(function() {
        $(".button-collapse").sideNav();
        $(".parallax").parallax();
        //Marks concentration button as selected if a concentration is selected
        concentration_name = $("#concentration-name").val();
        if (concentration_name != "") {
            var foundin = $('.btn-concentration-name:contains(' + concentration_name + ')');
            foundin.removeClass("red-text");
            foundin.removeClass("white");
            foundin.addClass("white-text");
            foundin.addClass("red");
        }
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
    if ($("#review").val() == "") {
        alert("Please add a review.");
        return false;
    }
    return true;
}

//Validates Add Course form
function validateAddCourseForm() {
    if ($("#course_id_add").val() == "" || $("#course_name_add").val() == "") {
        alert("Please fill in BOTH Course ID and Course Name fields.");
        return false;
    }
    return true;
}

//Linkedin Login Code
$("#btn-linkedinlogin").on("click", function() {
    IN.User.authorize(function() {});
})

function OnLinkedInFrameworkLoad() {
    IN.Event.on(IN, "auth", OnLinkedInAuth);
}

function OnLinkedInAuth() {
    IN.API.Profile("me").result(LoginUser);
}

function LoginUser(profiles) {
    var member = profiles.values[0];
    var userId = member.id;
    var firstName = member.firstName;
    var lastName = member.lastName;
    var photo = member.pictureUrl;
    if (userId != "") {
      console.log("Welcome", firstName);
      $("#user-id").val(userId);
      $("#first-name").val(firstName);
      $("#last-name").val(lastName);
      $("#photo").val(photo);
      $("#authenticate-login").submit();
    }
}

//Linkedin Logout code
$(".btn-logout").on("click", function() {
    if (IN.User.isAuthorized() == true) {
        console.log("Goodbye")
        IN.User.logout();
    }
    setTimeout(function() {
        location.href = "/logout";;
    }, 500);

})
