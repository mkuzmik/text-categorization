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

function recognize() {
    var result = document.getElementById('result');
    result.value = 'result here';
}