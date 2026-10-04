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
let currentMessage = null;

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
        // 交给渲染函数处理（高亮跟随 currentMessage）
        renderHistoryList(list);

    }catch(err){
        console.error("Error fetching history");
    }
}

// 根据当前对话信息(currentMessage)渲染历史列表并高亮当前项
function renderHistoryList(list){
    historyList.innerHTML = '';            // 清空旧列表（连同旧高亮）

    list.forEach(eachitem =>{
        const item = document.createElement("div");
        item.className = 'history-item';

        // 通过检测当前对话信息来决定是否高亮
        if(eachitem === currentMessage){
            item.classList.add('active');
        }
        item.textContent = eachitem;

        item.addEventListener('click', (e) => {
            currentMessage = eachitem;      // 更新当前对话信息
            renderHistoryList(list);        // 重渲染：去旧高亮、亮当前
            load_History_Message(eachitem);
        })

        const deleteBtn = document.createElement("button");
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = '🗑️';

        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            delete_History_Message(eachitem);
        })

        item.appendChild(deleteBtn);
        historyList.appendChild(item);
    })
}
// 加载消息
function load_History_Message(message){

}

function delete_History_Message(message){

}