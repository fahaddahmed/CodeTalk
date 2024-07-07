document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    const username = document.querySelector('#get-username').innerHTML;

    let room = "courses";
    joinRoom(room);

    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});

        document.querySelectorAll('.select-room').forEach(p => {
            p.style.color = "black";
        });
    }

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});

        document.querySelector('#display-message-section').innerHTML = '';
        document.querySelector('#user-message').focus();
    }

    function printMessage(message) {
        const paragraph = document.createElement('p');
        paragraph.setAttribute("class", "system-message");
        paragraph.innerHTML = message;
        document.querySelector('#display-message-section').append(paragraph);
        scrollDownChatWindow();

        document.querySelector("#user-message").focus();
    }

    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Sending messages
    document.querySelector('#send-message').onclick = () => {
        socket.emit('incoming-message', {'message': document.querySelector('#user-message').value, 'username': username, 'room': room });
        document.querySelector('#user-message').value = '';
    }

    // Display user message
    socket.on('message', data => {
        if(data.message) {
            const userParagraph = document.createElement('p');
            const usernameSpan = document.createElement('span');
            const currTime = document.createElement('span');
            const br = document.createElement('br');

            if (data.username == username) {
                userParagraph.setAttribute("class", "my-message");

                usernameSpan.setAttribute("class", "my-username");
                usernameSpan.innerHTML = data.username;

                currTime.setAttribute("class", "timestamp");
                currTime.innerHTML = data.time;

                userParagraph.innerHTML = usernameSpan.outerHTML + br.outerHTML + data.message + br.outerHTML + currTime.outerHTML + br.outerHTML;
            
                document.querySelector('#display-message-section').append(userParagraph);
            }
            else if (typeof data.username !== 'undefined') {
                userParagraph.setAttribute("class", "other-message");

                usernameSpan.setAttribute("class", "other-username");
                usernameSpan.innerHTML = data.username;

                currTime.setAttribute("class", "timestamp");
                currTime.innerHTML = data.time;

                userParagraph.innerHTML = usernameSpan.outerHTML + br.outerHTML + data.message + br.outerHTML + currTime.outerHTML + br.outerHTML;
            
                document.querySelector('#display-message-section').append(userParagraph);
            }
            else {
                printMessage(data.message);
            }
        }

        //scrollChat();
    });

    // Selecting a room


    /*


    FIX FOR BUTTONS


    
    */
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let selectedRoom = p.innerHTML;
            if (selectedRoom == room) {
                message = `You are already in ${room}.`;
                printMessage(message);
            }
            else {
                leaveRoom(room);
                joinRoom(selectedRoom);
                room = selectedRoom;
            }
        }
    });

    document.querySelector("#logout-btn").onclick = () => {
        leaveRoom(room);
    };

})
