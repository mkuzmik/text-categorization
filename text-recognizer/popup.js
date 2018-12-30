$(function(){
    $('#paste').click(function(){pasteSelection();});
});

$(function(){
    $('#recognize').click(function(){getResult();});
});

function pasteSelection() {
    chrome.tabs.query({active:true, windowId: chrome.windows.WINDOW_ID_CURRENT},
        function(tab) {
            chrome.tabs.sendMessage(tab[0].id, {method: "getSelection"},
                function(response){
                    const text = document.getElementById('text');
                    text.value = response.data;
                    M.textareaAutoResize(text);
                });
        });
}

const getParameters = () => {
    return new Promise(resolve => {
        chrome.storage.sync.get({
            // default values
            apiHost: 'http://localhost:5000',
            model: 'naive-bayes',
            size: '500'
        }, function (items) {
            resolve(items);
        });
    });
};

const recognize = async (text) => {
    const parameters = await getParameters();
    const urlWithParams = `${parameters.apiHost}/classify?q=${encodeURI(text)}&model=${parameters.model}&size=${parameters.size}`;
    const response = await fetch(urlWithParams);
    return await response.json();
};

async function getResult() {
    const result = document.getElementById('result');
    const text = document.getElementById('text');
    const xhr = new XMLHttpRequest();

    const res = await recognize(text.value);
    result.value = res.label;
}