// TODO: make parameters configurable
textRecognizerHost= 'http://localhost:5000/predict?size=500&q=';

function recognize(selectedText) {
    var xhr = new XMLHttpRequest();

    xhr.open("GET", textRecognizerHost + selectedText, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            alert(xhr.responseText);
        }
    };
    xhr.send();
}

chrome.contextMenus.create({
    title: "Recognize text",
    contexts:["selection"],
    onclick: function(info, tab) {
        recognize(info.selectionText);
    }
});