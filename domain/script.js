const dialogBox = document.querySelector(".dialog-box");
const sendBtn = document.querySelector("#dialog-send-btn");
const queryInput = document.querySelector("#query-input");

function sendMessage(){
    const text = queryInput.value.trim();

    if (!text) return;

    const msg = document.createElement("div");
    msg.className = 'msg userMsg';
    msg.innerHTML = '<div class="msg-user"></div>';
    msg.querySelector('.msg-user').textContent = text;
    dialogBox.appendChild(msg);
    queryInput.value = '';
    dialogBox.scrollTop = dialogBox.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);

queryInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter"&& !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

const sidebar = document.querySelector(".sidebar");
const sidebarCloseBtn = document.querySelector(".sidebar-close-btn");

sidebarCloseBtn.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
})

const historyList = document.querySelector(".history-list");

async function getMessage(){
    try{
        const res = await fetch('http://localhost:8080/api/getHistoryList');
        if (!res.ok) {
            throw new Error("Network response was not ok");
        }
        const list = await res.json();
        if (!Array.isArray(list)) {
            throw new Error("Invalid response format");
        }
        list.forEach(item =>{
            const div = document.createElement("div");
            div.className = 'history-item';
            div.textContent = item;
            historyList.appendChild(div);
        })

    }catch(err){
        console.error("Error fetching history");
    }
}