function save_options() {
    var apiHost = document.getElementById('api-host').value;
    var model = document.getElementById('model').value;
    var size = document.getElementById('size').value;
    chrome.storage.sync.set({
        apiHost: apiHost,
        model: model,
        size: size
    }, () => {
        let statusDiv = document.getElementById('status');
        statusDiv.innerHTML = 'Saved';
        setTimeout(() => statusDiv.innerHTML = '', 750);
    });
}

function restore_options() {
    chrome.storage.sync.get({
        // default values
        apiHost: 'http://localhost:5000',
        model: 'naive-bayes',
        size: '500'
    }, function(items) {
        document.getElementById('api-host').value = items.apiHost;
        document.getElementById('model').value = items.model;
        document.getElementById('size').value = items.size;
    });
}

document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click', save_options);