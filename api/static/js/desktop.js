/**
 * Created by christian.cecilia1@gmail.com on 6/16/16.
 */
var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
var current_page = $("#current_page").val();

//set csrf token
$.ajaxSetup({
    beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

//New Task Form
// services
function serviceClicked(service_id){
    console.log("service clicked");
    console.log(service_id);
    $(".service-link").each(function(){
        console.log($(this).attr('data-id'));
        if( $(this).attr('data-id') == service_id){
            console.log("is selected");
            $(this).css("opacity","1");
            $.post('/getServiceOptions/', {service_id: service_id}, function (response) {
                if( response.status === "success" ){
                    console.log("got service options");
                    console.log(response.options);
                    options = response.options;
                    for (i = 0; i < options.length; i++) {
                        html =  "<li>" +
                                    "<label for='option-"+options[i].id+"'>"+options[i].name+ "</label>" +
                                    "<input id='option-"+options[i].id+"' type='radio' class='option-radio' value='"+options[i].id+"' onchange='optionClicked("+options[i].id+")'/>" +
                                "</li>";
                        $(html).appendTo(".options-list-horizontal");
                    }
                }
            }, "json");
            $('.service-options').show();
        }else{
            $(this).css("opacity",".5");
        }
    });
}

function optionClicked(option_id) {
    console.log("option "+option_id+" clicked");
    $.post('/getOptionInputs/', {option_id: option_id}, function (response) {
        if( response.status === "success" ){
            console.log("got inputs");
            console.log(response.input_html);
            input_html = response.input_html;
            for (i = 0; i < input_html.length; i++) {
                $(input_html[i]).appendTo(".options-list-horizontal");
            }
            if( response.map_required === "True" ){
                console.log("map required");
                //$("").insertAfter(".options-list-horizontal");
                //initMap();
                $('#map').show();
            }else{
               console.log("map not required")
            }
        }else{
            console.log("get inputs failed");
        }
    }, "json");
}




$(document).ready(function(){
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

    //Main Groups
    $(".add-main-grouping").click(function(){
        $(".add-main-grouping-input").css("display","inline-block");
    });

    $("#add-main-grouping-button").click(function(){
        group_name = $("input[name='main-group-name']");
        if( group_name.val() !== ""){
            params = {
                name: group_name.val()
            };
            $.post('/addMainGroup/', params, function (response) {
                if(response.status === "success"){
                    $(".add-main-grouping-input").empty();
                    $(".add-main-grouping-input").text("main group added");
                    setTimeout(function () {
                        location.reload();
                    },5000)
                }
            }, "json")
        }else{
            group_name.css("border","1px solid red");
        }

    });


    //Calender
    $("#calendar").fullCalendar({
        // put your options and callbacks here
    });

    //New Task Form
    $(".type-select").change(function(){
        console.log("type changed");
        services_row = $(".task-services");
        type_id = $(".type-option").filter(":selected").val();

        //reset services
        services_row.empty();
        services_row.hide();

        if( type_id == 0 ){
            console.log("type none selected");
            $("#service-legend").hide();
            services_row.hide();
        }else if( type_id == 2 ){
            console.log(type_id);
            services_row.show();
            $("<legend>Time</legend>").appendTo(services_row);
            
        }else{
            console.log("type selected");
            console.log(type_id);
            services_row.show();
            $("<legend id='service-legend'>Services</legend>").appendTo(services_row);
            $("<ul class='services-list'></ul>").insertAfter("#service-legend");
            $.post('/getServices/', {type_id: type_id}, function (response) {
                if( response.status === "success" ){
                    console.log("got services");
                    console.log(response.services);
                    services_list = response.services;
                    console.log(services_list.length);
                    for (i = 0; i < services_list.length; i++) {
                        listHtml = "<li>" +
                                        "<a class='service-link' onclick='serviceClicked("+services_list[i].id+")' data-id='"+services_list[i].id+"'>" +
                                            "<img class='service-thumbnail' src='"+services_list[i].logo_image_url+"' alt='"+services_list[i].name+"'/>" +
                                        "</a>"+
                                    "</li>";
                        $(listHtml).appendTo(".services-list");
                    }
                }else{
                    console.log("failed to get services");
                }
            }, "json");
        }
    });

    $(".option-radio").click(function(){
        console.log("option clicked");
    });
});
