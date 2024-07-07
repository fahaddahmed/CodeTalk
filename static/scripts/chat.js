document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#show-sidebar-button').onclick = () => {
        document.querySelector('#sidebar').classList.toggle('view-sidebar');
    };

    let message = document.querySelector('#user-message');
    message.addEventListener('keyup', event => {
        event.preventDefault();

        if (event.keyCode === 13) { // 13 keycode == enter key
            document.querySelector('#send-message').click();
        }
    });
});
