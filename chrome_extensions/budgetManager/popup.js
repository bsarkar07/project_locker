console.log("hi");

let limit=0;
let total=0;
let limit_msgId="limitRelatedMessage";
let badgeId="setBadge";

function limitExceed(sum,lim){
    if(sum>lim) return true;
    else return false;
}


chrome.storage.sync.get(["total","limit"],function(storage){
    if(storage.total)
        total=parseFloat(storage.total);
    $("#spent").text(total);

    if(storage.limit)
        limit=parseFloat(storage.limit);
    $("#limit").text(limit);
});

$("#submit-btn").click(function(){
    console.log("clicked");
    let get_data=0;
    let value=parseFloat($("#amount").val());
    if(!isNaN(value)){
        if(limit){
            if(limitExceed(total+value,limit)){
                chrome.runtime.sendMessage({id:limit_msgId,description:"Exceeding set limit, amount not added!"});
                console.log("linmit exceeded notif sent");
            }
            else
                total+=value;
        }
        else{
            chrome.runtime.sendMessage({id:limit_msgId,description:"Set limit in options page"});
            console.log("limitnot set notif sent");
        }
        chrome.storage.sync.set({"total":total});
        chrome.runtime.sendMessage({id:badgeId,data:total});
        $("#spent").text(total);
    }
});

// chrome.runtime.onMessage.addListener(function(message,sender,response){
//     if(message.msg=="toAddNumber"){
//         let data=message.data;
//         if(limitExceed(total+))
//     }
// })
