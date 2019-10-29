$(function(){
    // When we're using HTTPS, use WSS too.
    // var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    // var chatSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    var chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + roomName + '/');
        console.error('Chat socket closed unexpectedly');

        
    // onmessage는 counsumers에서 보내는 메세지를 받는 부분이다.
    chatSocket.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")//table id
        var ele = $('<tr></tr>')

        ele.append(
            $("<td></td>").text(data.timestamp)
        )
        ele.append(
            $("<td></td>").text(data.handle)
        )
        ele.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(ele)//chat table + ele
    };

    // socket의 연결이 끊어지면 일어날 행동을 정의하는 부분이다.
    chatSocket.onclose = function(event) {
        console.error('Chat socket closed unexpectedly');
    };


    // document.querySelector('#chat-message-input').focus();
    // document.querySelector('#chat-message-input').onkeyup = function(e) {
    //     if (e.keyCode === 13) {  // enter, return
    //         document.querySelector('#chat-message-submit').click();
    //     }
    // };

    $("#chatform").on("submit", function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chatSocket.send(JSON.stringify({//JSON 포맷으로 chatSocket에 전달
            'message': message
        }));
        $("#message").val('').focus();// message 값 초기화
        return false;
    });
});