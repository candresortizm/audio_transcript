document.addEventListener("DOMContentLoaded", () => {
    loadChatHistory();
});

function addMessage(text, className, sentiment) {
    let chatBody = document.getElementById("chatBody");
    let messageDiv = document.createElement("div");
    let icon_sentiment = document.createElement("i");
    switch (sentiment) {
        case "positive":
            icon_sentiment.classList.add("fa","fa-check-circle");
            break;
        case "negative":
            icon_sentiment.classList.add("fa","fa-times-circle");
            break;
        case "neutral":
            icon_sentiment.classList.add("fa","fa-minus-circle");
            break;
    }
    messageDiv.classList.add("message", className);
    messageDiv.innerHTML = "<span>"+text+"</span>";
    messageDiv.appendChild(icon_sentiment);
    chatBody.appendChild(messageDiv);
}

function loadChatHistory() {
    let chatBody = document.getElementById("chatBody");
    let messages = JSON.parse(jsonfile || "[]");
    messages.forEach(msg => addMessage(msg.texto, msg.clase,msg.sentimiento));
}