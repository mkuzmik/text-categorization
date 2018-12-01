// TODO: make parameters configurable
defaultApiHost = 'http://localhost:5000';
endpoint = '/predict?size=500&q=';

const getHost = () => {
    return new Promise((resolve, reject) =>
        chrome.storage.local.get(['apiHost'], function (result) {
            resolve(result.apiHost);
        }));
};

const recognize = async (selectedText) => {
    const apiHost = await getHost() || defaultApiHost;
    const response = await fetch(apiHost + endpoint + encodeURI(selectedText));
    const body = await response.json();
    alert(body);
};

chrome.contextMenus.create({
    title: "Recognize text",
    contexts: ["selection"],
    onclick: function (info, tab) {
        recognize(info.selectionText);
    }
});