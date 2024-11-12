$(document).ready(function() {
    const userId = "{{ user_id }}";  // Get the user ID from Flask template
    const pollingInterval = 1000;  // Set polling interval to 1 second
    let autoScrollEnabled = true;  // Flag to enable/disable auto-scroll

    // Function to load and display messages from the server
    function loadMessages() {
        $.get('/get_messages', function(data) {
            const chatBox = $('#chat-box');
            const shouldAutoScroll = chatBox.scrollTop() + chatBox.innerHeight() >= chatBox[0].scrollHeight - 20;

            chatBox.empty();  // Clear the chat box
            
            // Ensure the messages are displayed in the correct order (oldest to newest)
            data.forEach(message => {
                const messageHtml = message.user === userId ? 
                    `<div class="chat-message self">
                        <span class="timestamp">${message.timestamp}</span>
                        <span class="message">${message.message}</span>
                    </div>` :
                    `<div class="chat-message">
                        <span class="timestamp">${message.timestamp} (${message.user}):</span>
                        <span class="message">${message.message}</span>
                    </div>`;
                chatBox.append(messageHtml);
            });

            // If auto-scroll is enabled, scroll to the bottom
            if (autoScrollEnabled && shouldAutoScroll) {
                chatBox.scrollTop(chatBox[0].scrollHeight);
            }
        });
    }

    // Function to send a new message to the server
    function sendMessage() {
        const message = $('#message-input').val();
        if (message.trim() !== '') {
            $.post('/send_message', { message: message }, function() {
                $('#message-input').val('');  // Clear input after sending
                loadMessages();  // Reload the messages after sending
            });
        }
    }

    // Event listener for the Send button
    $('#send-btn').click(function() {
        sendMessage();
    });

    // Allow pressing Enter to send a message
    $('#message-input').keypress(function(e) {
        if (e.which === 13) {  // Enter key
            sendMessage();
        }
    });

    // Track user scrolling to disable auto-scroll when they scroll up
    $('#chat-box').on('scroll', function() {
        const chatBox = $(this);
        if (chatBox.scrollTop() + chatBox.innerHeight() >= chatBox[0].scrollHeight - 20) {
            autoScrollEnabled = true;  // Re-enable auto-scroll when user reaches the bottom
        } else {
            autoScrollEnabled = false;  // Disable auto-scroll when user scrolls up
        }
    });

    // Automatically poll the server for new messages every second
    setInterval(loadMessages, pollingInterval);

    // Initial load of messages when the page is first loaded
    loadMessages();
});
