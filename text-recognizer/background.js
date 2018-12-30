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

chrome.contextMenus.create({
    title: "Recognize text",
    contexts: ["selection"],
    onclick: async (info) => {
        const blob = await recognize(info.selectionText);
        alert(JSON.stringify(blob));
    }
});