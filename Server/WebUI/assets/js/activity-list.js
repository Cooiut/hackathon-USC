let login_mode = false;

let BASE_URL = "/";

$.ajax({
    datatype: "json",
    url: BASE_URL + "api/user/getinfo",
    method: "GET",
    success: (resp) => {
        $('#username').html(JSON.parse(resp)['username']);
    }
})

$.ajax({
    datatype: "json",
    url: BASE_URL + "api/user/getnum",
    method: "GET",
    success: (resp) => {
        $('#total-user-num').html(JSON.parse(resp)['total'])
    }
})

