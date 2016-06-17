/**
 * Created by christian.cecilia1@gmail.com on 6/16/16.
 */

$(document).ready(function(){
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    //set csrf token
    $.ajaxSetup({
        beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    $("#show-register,#show-login").click(function(){
        $("#login-form").slideToggle();
        $("#register-form").slideToggle();
    });

    $("#register-submit-btn").click(function(){
        username = $("#register-username");
        email = $("#register-email");
        password = $("#register-password");
        confirm_password = $("#register-pw-confirm");

        if(username.val() === ""){
            username.css("border","1px solid red");
        }else if(email.val() === ""){
            email.css("border","1px solid red");
        }else if(password.val() !== confirm_password.val()){
            password.css("border","1px solid red");
            confirm_password.css("border","1px solid red");
        }else{
            params = {
                username: username.val(),
                email: email.val(),
                password: password.val()
            };
            console.log(params);
            $.post('/registerUser/', params, function (response) {
                if (response.status === "success") {
                    window.alert("You registered");
                }
                else if(response.status === "fail"){
                    window.alert(response.error_message);
                }
            }, "json")
        }
    });

});
