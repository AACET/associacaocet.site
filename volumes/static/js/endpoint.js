const getHeaders = async (name, callback) => {
    let req = new XMLHttpRequest();
    req.open('GET', document.location, false);
    req.send(null);
    let headers = req.getAllResponseHeaders().toLowerCase();
    for (header of headers.split("\r\n")) {
        let [k, v] = header.split(": ");
        if (k == name.toLowerCase()) {callback(v); break;}
    }
}

addEventListener("load", (event) => {
    for (element of document.getElementsByClassName("display-container")[0].childNodes) {$(element).hide();}
    
    getHeaders("X-Endpoint-Server", (endpoint) => {document.getElementById("endpoint").innerText = endpoint != null ? ': '+endpoint : '';});
    
    let i = 500;
    $(document.getElementsByClassName("display-container")[0]).show();
    for (element of document.getElementsByClassName("display-container")[0].childNodes) {
        $(element).fadeIn(i);
        i += 350
    }
});