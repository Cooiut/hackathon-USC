$(".username").html("Test")

$("#option-store").click(() => {
    $("#balance").hide();
    $("#store").show();
    $("#option-store").attr("active", "");
    $("#option-balance").removeAttr("active");
})

$("#option-balance").click(() => {
    $("#balance").show();
    $("#store").hide();
    $("#option-balance").attr("active", "");
    $("#option-store").removeAttr("active");
})