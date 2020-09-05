let login_mode = false;

let BASE_URL = "/";

$("#login-btn").click(() => {
    if (!login_mode) {
        $("#welcome-words").css({
            "opacity" : "0",
            "transition" : "opacity 1s ease-in-out"
        });
        setTimeout(() => {
            $("#welcome-words").hide();
            $("#login-holder").show();
        }, 1000);
        login_mode = true;
    } else {
        $.ajax({
            url: BASE_URL + "api/login",
            method: "POST",
            data: $("form").serialize(),
            success: (resp) => {
                console.log(resp);
            }
        })
    }
});