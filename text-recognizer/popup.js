$(function(){
    $('#paste').click(function(){pasteSelection();});
});

$(function(){
    $('#recognize').click(function(){recognize();});
});

function pasteSelection() {
    chrome.tabs.query({active:true, windowId: chrome.windows.WINDOW_ID_CURRENT},
        function(tab) {
            chrome.tabs.sendMessage(tab[0].id, {method: "getSelection"},
                function(response){
                    var text = document.getElementById('text');
                    text.innerHTML = response.data;
                    M.textareaAutoResize(text);
                });
        });
}

// TODO: make parameters configurable
textRecognizerHost= 'http://localhost:5000/predict?size=200&q=';

function recognize() {
    var result = document.getElementById('result');
    var text = document.getElementById('text');
    var xhr = new XMLHttpRequest();

    xhr.open("GET", textRecognizerHost + text.innerHTML, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            result.value = xhr.responseText;
        }
    };
    xhr.send();
}