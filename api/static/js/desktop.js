/**
 * Created by christian.cecilia1@gmail.com on 6/16/16.
 */

$(document).ready(function(){
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    var current_page = $("#current_page").val();

    //set csrf token
    $.ajaxSetup({
        beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    //Register/Login Form Toggle
    $("#show-register,#show-login").click(function(){
        $("#login-form").slideToggle();
        $("#register-form").slideToggle();
    });

    //Register
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
                    username.css("border","1px solid green");
                    email.css("border","1px solid green");
                    password.css("border","1px solid green");
                    confirm_password.css("border","1px solid green");
                    window.location.replace("/dashboard/"+response.user_id+"/");
                }
                else if(response.status === "fail"){
                    window.alert(response.error_message);
                }
            }, "json")
        }
    });

    //Login
    $("#login-btn").click(function(){
        email = $("#login-email");
        password = $("#login-password");

        if(email.val() === "" || password.val() === ""){
            email.css("border","1px solid red");
            password.css("border","1px solid red");
        }else{
            params = {
                email: email.val(),
                password: password.val()
            };
            $.post('/loginAjax/', params, function (response) {
                 if(response.status === "fail" && response.error === "email_error"){
                     email.css("border","1px solid red");
                 }else if(response.status === "fail" && response.error === "password_error"){
                     password.css("border","1px solid red");
                 }else if(response.status === "fail" && response.error === "verification_error"){
                     $("#verify-email-popup p").text(response.error_message);
                     $("#verify-email-popup").slideDown();
                 }else if(response.status === "success"){
                     window.location.replace("/dashboard/"+response.user_id+"/");
                 }
            }, "json")
        }
    });

    //Nav
    $(".nav-link").click(function(){
        $(".nav-link").removeClass("active");
        $(this).addClass("active");
    });

});
