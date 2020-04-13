
$(document).ready(function(){
$("#link-btn").click(function(event) {
    event.preventDefault();
    var email = $("#email").val();
    console.log(email);
    
    $.ajax({ 
        type:'POST',
        url: 'http://localhost:8000/reset/password-link/',
        data: {
            "email":email,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        dataType: 'json',
        success: function () {
            alert("check your email");
        },
        error:function(jqXHR){
            alert(jqXHR.responseText);
        }
        
        
    });

    });
});

$(document).ready(function(){
$("#login-btn").click(function (event) {
    event.preventDefault();
    var username = $("#username").val();
    var password = $("#password").val();
    
    $.ajax({ 
        type:'POST',
        url: 'http://localhost:8000/login/',
        data: {
            "username": username,
            "password": password,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        dataType: 'json',
        success: function (data,status, xhr) {
            // console.log(xhr.status);
            alert("logged in");
        },
        error:function(){
            
            alert("Invalid Credentials")
        }
      
    });

  });
});

$(document).ready(function(){
    $("#register-btn").click(function (event) {
        event.preventDefault();
        var username = $("#username").val();
        var email = $("#email").val();
        var password1 = $("#password1").val();
        var password2 = $("#password2").val();

        var username_pattern = /^[a-zA-Z]+[0-9]*[a-zA-Z]*$/;
        var password_pattern = /^[a-zA-Z0-9@$#%]*[@$#%]+[a-zA-Z0-9@$#%]*$/;
        
        if (username == " " || email == " " || password1 == " " || password2 == " "){
            alert("Every field should be filled");
            return;
            
        } else if(! username_pattern.test(username)){
            alert("username should not begin with integer ");
            return ;
        }
        if (password1 === password2){
            if((!password_pattern.test(password1)) && password1.length < 6){
                alert("should have length atleast one special character and length is minimum 6")
                return
            }
        }
        else{
            alert("Both the passwords should match")
            return;
       } 
        
        $.ajax({ 
            type:'POST',
            url: 'http://localhost:8000/',
            data: {
                "username": username,
                "email" : email,
                "password1": password1,
                "password2": password2,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            dataType: 'json',
            success: function (data) {
                alert("Registered Successfully");
            },
            error:function(jqXHR){
                alert(jqXHR.responseText);
            }
          
        });
    
      });
    });

$(document).ready(function(){
    $("#password-btn").click(function (event) {
        event.preventDefault();
        
        var email = $("#email").val();
        var password1 = $("#password1").val();
        var password2 = $("#password2").val();

        
        var password_pattern = /^[a-zA-Z0-9@$#%]*[@$#%]+[a-zA-Z0-9@$#%]*$/;
        
        if ( password1 == " " || password2 == " "){
            alert("Every field should be filled");
            return;
            
        } 
        if (password1 === password2){
            if((!password_pattern.test(password1)) && password1.length < 6){
                alert("should have length atleast one special character and length is minimum 6")
                return
            }
        }
        else{
            alert("Both the passwords should match")
            return;
        } 
        
        $.ajax({ 
            type:'POST',
            url: 'http://localhost:8000/reset/password/<str:url>',
            data: {
                "email" : email,
                "password1": password1,
                "password2": password2,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            dataType: 'json',
            success: function (data) {
                alert("Password Changed Successfully");
            },
            
            
        });
    
        });
    });
