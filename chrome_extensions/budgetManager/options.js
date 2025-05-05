let new_limit=$("#new_limit");
let submit_limit=$("#submit_limit");
let reset=$("#reset");

submit_limit.click(function(){
    let val=parseInt(new_limit.val());
    chrome.storage.sync.set({"limit":val});
    chrome.runtime.sendMessage({id:"limitRelatedMessage",description:"New limit set!"});
    // close();
});

reset.click(function(){
    chrome.storage.sync.set({"total":0});
    chrome.runtime.sendMessage({id:"reset",description:"Amount has been reset!"});
    // close();
});
