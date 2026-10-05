const dialogBox = document.querySelector(".dialog-box");
const sendBtn = document.querySelector("#dialog-send-btn");
const queryInput = document.querySelector("#query-input");

function sendMessage(){
    const text = queryInput.value.trim();

    if (!text) return;

    // 确保有会话 id，没有就用系统时间生成
    ensureCurrentMessage();

    // 渲染用户消息（复用封装函数）
    appendMessage('user', text);
    queryInput.value = '';
    dialogBox.scrollTop = dialogBox.scrollHeight;
    
    // 保存用户消息
    saveMessage(text, 'user');

    // 请求 AI 回复并渲染、保存
    (async () => {
        const aimsg = await getAIresponse(text);
        appendMessage('ai', aimsg);
        saveMessage(aimsg, 'ai');
    })();
}

// 保存一条消息到当前会话
async function saveMessage(text, role){
    if(!text || !currentMessage) return;   // 没有会话就不存

    await fetch('http://localhost:8080/api/saveMessage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            id: currentMessage,
            role: role,
            message: text
        })
    });
}

// 请求 AI 回复
async function getAIresponse(text){
    const response = await fetch('http://localhost:8080/api/getAIresponse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: text,
            id: currentMessage
        })
    });
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data.content;
}

function ensureCurrentMessage(){
    if(!currentMessage){
        currentMessage = '对话' + Date.now();
    }
}

function appendMessage(role, content){
    const msg = document.createElement("div");

    if(role === 'ai'){
        msg.className = 'msg aiMsg';
        msg.innerHTML = '<div class="msg-ai"></div>';
        msg.querySelector('.msg-ai').textContent = content;
    } else if(role === 'user'){
        msg.className = 'msg userMsg';
        msg.innerHTML = '<div class="msg-user"></div>';
        msg.querySelector('.msg-user').textContent = content;
    }

    dialogBox.appendChild(msg);
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

async function getHistoryListAsync(){
    try{
        const res = await fetch('http://localhost:8080/api/getHistoryList');
        if (!res.ok) {
            throw new Error("Network response was not ok");
        }
        const list = await res.json();
        if (!Array.isArray(list)) {
            throw new Error("Invalid response format");
        }
        renderHistoryList(list);

    }catch(err){
        console.error("Error fetching history");
    }
}

function renderHistoryList(list){
    historyList.innerHTML = '<div class="history-list-title">历史消息</div>';            // 清空旧列表（连同旧高亮）

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
async function load_History_Message(message){
    dialogBox.innerHTML = '';

    const res = await fetch(`http://localhost:8080/api/getHistoryMsg?id=${encodeURIComponent(message)}`);
    if (!res.ok) {
        throw new Error("Network response was not ok");
    }
    const msgList = await res.json();

    for (const item of msgList){
        appendMessage(item.role, item.content);
    }
}

// 删除历史会话
async function delete_History_Message(id){
    // 1. 调后端删除接口（删掉对应会话文件）
    const res = await fetch(`http://localhost:8080/api/deleteChat?id=${encodeURIComponent(id)}`, {
        method: 'DELETE'
    });
    if (!res.ok) {
        throw new Error("Network response was not ok");
    }

    if (id === currentMessage) {
        currentMessage = null;
        dialogBox.innerHTML = '';
        new_dialog();
    }

    await getHistoryListAsync();
}

const newDialogBtn = document.querySelector(".new-dialog-btn");
const newKnowledgeBtn = document.querySelector(".add-knowledge-btn");

function new_dialog(){

}
newDialogBtn.addEventListener("click", new_dialog);

function add_knowledge(){

}
newKnowledgeBtn.addEventListener("click", add_knowledge);

// 页面加载后自动加载历史对话列表
getHistoryListAsync();