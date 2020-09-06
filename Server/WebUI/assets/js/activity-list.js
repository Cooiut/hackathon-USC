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
        $('#total-user-num').html(JSON.parse(resp)['total']);
    }
})

$.ajax({
    url: BASE_URL + "api/user/enrolled_detail",
    method: "GET",
    success: (resp) => {
        resp = JSON.parse(resp);
        for (let act_id of resp["act_ids"]) {
            console.log(act_id);
            $.ajax()
        }
    }
})