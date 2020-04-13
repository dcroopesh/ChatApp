$(document).ready(function(){
    var sender = $("#get-sender").text();
    var receiver=""
    $(".user-list").click(function(event) {
        event.preventDefault();
        receiver = $(this).attr("id");
        $.ajax({
            type:'GET',
            url: "",
            data:{
                receiver:$(this).attr('id'),
                
            },
            success: function () {
                $(".shadow").hide();
                $("#receiver").text(receiver);

            },
            error:function(jqXHR){
                alert(jqXHR.responseText);
               
            }
        });
        
        $(".room").empty();
        
        const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/p2pchat/' +  "room" + '/');
        

        chatSocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            var message_element = $("<p></p>").html(data.message );
            
            if (sender === data.username){
                $(message_element.css({"position":"absolute","margin":"20px","right":"0","background-color": "#9bc7dd","font-family":"monospace","font-size":"21px","border-radius":"5px" })).appendTo(".room");
                $("<br/>").appendTo(".room");
                
            }
            else{
                $(message_element.css({"position":"absolute","margin":"20px","left":"0","background-color": "#8fd3a9","font-size":"21px","border-radius":"5px"})).appendTo(".room");
                $("<br/>").appendTo(".room");
                
            }
        };
        
        $(".abc").click(function (){
                chatSocket.close();
        });

        
        $("#message-text").keyup( function(event) {
            if(event.which == 13){
            $("#submit").click();
            }
        });


        $("#submit").click( function(event) {
            const messageInput = $("message-text").val();
            console.log(messageInput);
            chatSocket.send(JSON.stringify({
                'message': messageInput
            }));
            $("message-text").val("");
        });
    
});
});