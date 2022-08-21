$(document).ready(function(){
    // make socket object
    var socket = io();

    let room = 'lounge';
    joinRoom(room);

    // show message on receiving message in 'message' event bucket
    socket.on('message',function(data){
        
        // if message is sent by current user
        if (data.username == username) {
            printUserMsg(data, 1);
        }
        // if message is received form some other user
        else if (data.username) {
            printUserMsg(data, 0);
        }
        // if message is system generated
        else {
            printSysMsg(data.msg);
        }
        
        // scroll chat window automatically
        scrollDownChatWindow();
    });

    // send message on pressing submit button
    $('#send_message').click(function(){
        // console.log($('#user_message').val())
        // console.log(room);
        socket.send({'msg': $('#user_message').val(), 'username': username, 'room': room});
        // Clear the input area
        $('#user_message').val("");
    });

    // send message on pressing 'enter'
    $('#user_message').keypress(function(e){
        if(e.keyCode==13){
            // console.log($('#user_message').val())
            // console.log(room);
            socket.send({'msg': $('#user_message').val(), 'username': username, 'room': room});
            // Clear the input area
            $('#user_message').val("");
        }
    });

    $('.select-room').each(function(){
        $( this ).click(function(e){              // Important NOTE: don't forget to keep space in $() with 'this' keyword, otherwise it will give unexpected behaviour
            let newRoom = this.innerHTML.toLowerCase();
            console.log(newRoom);
            // console.log(this);
            console.log(newRoom, room);
            if (newRoom == room) {
                // msg = `You already in ${room} room.`;
                // printSysMsg(msg);
            }
            else {
                leaveRoom(room);
                joinRoom(newRoom);
                // msg = `You entered in ${room} room.`;
                room = newRoom;
                // printSysMsg(msg);
            }
        })
    });

    $("#logout-btn").click(function(){
        leaveRoom(room);
    })

    // Leave Room function
    function leaveRoom(room) {
        // console.log(room)
        $('.select-room').each(function () {
            $( this ).css("color", "black");
          })
        socket.emit('leave', {'username': username, 'room': room});
    };

    // Join Room function
    function joinRoom(room) {
        // console.log(room)
        console.log('#'+CSS.escape(room));
        $('#'+CSS.escape(room)).css('color', "#ffc107");
        $('#'+CSS.escape(room)).css('backgroundColor', 'white');
        socket.emit('join', {'username': username, 'room': room});
        // Clear message area
        $('#display-chat-section').empty();
        // Autofocus to input area whenever user joins a room
        $('#user_message').focus();
    };

    // Print system messages
    function printSysMsg(msg) {
        var sys_msg = $('<p class="system-msg"></p>').text(msg);
        $('#display-chat-section').append(sys_msg);
    }

    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-chat-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function printUserMsg(msg, curr_user) {
        var message = $("<div class=\"msg-text\"></div>").text(msg.msg)
        var username_span = $("<div class=\"msg-info-name\"></div>").text(msg.username)
        var timestamp_span = $("<div class=\"msg-info-time\"></div>").text(msg.timestamp)
        var message_info = $("<div class=\"msg-info\"></div>").append(username_span, timestamp_span);
        var message_bubble = $("<div class=\"msg-bubble\"></div>").append(message_info, message);
        if (curr_user == 1) var message_div = $("<div class=\"msg right-msg\"></div>").append(message_bubble);
        else var message_div = $("<div class=\"msg left-msg\"></div>").append(message_bubble);
        $('#display-chat-section').append(message_div);
        // console.log(current_user);
    }
})