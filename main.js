function webSocketCallback(event) {
    console.log(event.data);
    const msg = JSON.parse(event.data)
    switch (msg.type) {
        case "values":
            updateTable("valueTable", msg.values);
            break;    
    }
}

function setupWebSocket() {
    socket = new WebSocket("ws://" + window.location.host);
    socket.onmessage = webSocketCallback;
    return socket;
} 

function updateTable(id, data){
    let tableBody = document.getElementById(id).getElementsByTagName("tBody")[0];
    let tableRows = data.map(item => {
        let tr = document.createElement("tr");
        //console.log(item);
        
        let nameTd = document.createElement("td");
        nameTd.innerHTML = item.name; 
        tr.appendChild(nameTd);
        
        let valTd = document.createElement("td");
        valTd.innerHTML = item.value; 
        tr.appendChild(valTd);
        return tr;
    });
    tableBody.replaceChildren(...tableRows);
}