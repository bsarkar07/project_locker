let contextMenuObj={
    title:"Add to spendings",
    id:"AddToSpendings",
    contexts:["selection"]
};

let limit_msgId="limitRelatedMessage";
let reset_msgId="reset";
let badgeId="setBadge";

function sendNotif(id,message){
    let obj={
        type:"basic",
        iconUrl:"icon48.png",
        title:"Limit",
        message:message
    };
    chrome.notifications.create(id,obj);
    chrome.notifications.clear(id);
}

function limitExceed(sum,lim){
    if(sum>lim) return true;
    else return false;
}

function setBadge(data){
    console.log(parseFloat(data));
    data=parseFloat(data);
    chrome.browserAction.setBadgeText({text:data},function(e){
        console.log(e);
    });
    chrome.browserAction.setBadgeBackgroundColor({color:"#fff"},function(){
        console.log("color set");
    })
}

chrome.contextMenus.create(contextMenuObj);
// chrome.contextMenus.onClicked.addListener(function(clickData){
//     console.log(clickData);
// });

chrome.contextMenus.onClicked.addListener(function(clickData){
    // if(!parseFloat(clickData.selectionText))
    // console.log("in if");
    let text=parseFloat(clickData.selectionText);
    if(clickData.menuItemId=="AddToSpendings" && text){
        chrome.storage.sync.get(["total","limit"],function(storage){
            let newTotal=storage.total+parseFloat(text);
            if(storage.limit){
                console.log("in if");
                if(limitExceed(newTotal,storage.limit))
                    sendNotif(limit_msgId,"Exceeding set limit, amount not added!");
                else{
                    chrome.storage.sync.set({"total":newTotal});
                    setBadge(newTotal);
                }
            }
            else
                sendNotif(limit_msgId,"Set limit in options page");
        });
    }
});

chrome.runtime.onMessage.addListener(function(message,sender,response){
    if(message.id==limit_msgId||message.id==reset_msgId)
        sendNotif(message.id,message.description);

    if(message.id==badgeId)
        setBadge(message.data);
});

// chrome.storage.onChanged.addListener(function(changes,storageName){
//     console.log(changes.total.newValue);
//     chro
// });
