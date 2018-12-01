$(function(){
    $('#paste').click(function(){pasteSelection();});
});

$(function(){
    $('#recognize').click(function(){recognize();});
});

$(function(){
    $('#apiHost').change(function(){storeApiHost();});
});

const getHostAsync = () => {
    return new Promise((resolve, reject) =>
        chrome.storage.local.get(['apiHost'], function (result) {
            resolve(result.apiHost);
        }));
};

const getApiHost = async () => {
    var apiHost = document.getElementById('apiHost');
    let hostFromStorage = await getHostAsync();
    apiHost.innerHTML = hostFromStorage || defaultApiHost;
};

$(document).ready(function() {
    getApiHost();
});

function pasteSelection() {
    chrome.tabs.query({active:true, windowId: chrome.windows.WINDOW_ID_CURRENT},
        function(tab) {
            chrome.tabs.sendMessage(tab[0].id, {method: "getSelection"},
                function(response){
                    var text = document.getElementById('text');
                    text.value = response.data;
                    M.textareaAutoResize(text);
                });
        });
}

// TODO: make parameters configurable
endpoint = '/predict?size=500&q=';
defaultApiHost = 'http://localhost:5000';

function recognize() {
    var result = document.getElementById('result');
    var text = document.getElementById('text');
    var xhr = new XMLHttpRequest();

    xhr.open("GET", getHost() + endpoint + text.value, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            result.value = xhr.responseText;
        }
    };
    xhr.send();
}

function getHost() {
    var apiHost = document.getElementById('apiHost');
    return apiHost.value && apiHost.value.trim() ? apiHost.value : defaultApiHost;
}

function storeApiHost() {
    var apiHost = document.getElementById('apiHost');
    chrome.storage.local.set({apiHost: apiHost.value});
}