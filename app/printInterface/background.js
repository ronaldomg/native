/*
 * Listens for the app launching, then creates the window.
 *
 * @see http://developer.chrome.com/apps/app.runtime.html
 * @see http://developer.chrome.com/apps/app.window.html
 */

chrome.tabs.onSelectionChanged.addListener(function(tabid){showMe(tabid);});
chrome.tabs.onUpdated.addListener(function(tabid){showMe(tabid);});
function showMe(tabId){
  chrome.tabs.get(tabId, function(cTab){
    if (cTab.url.indexOf('hemi') > -1){
      chrome.pageAction.show(tabId);
     }else{
      chrome.pageAction.hide(tabId);
    }

});
}

/*******Begin Native connection handlers**********/
var nativeHost = 'br.com.bluefocus.printhost';
var port = null; //global port for native connections null for inactive
var i = 0; //global counter for controlling native connection retries

/**
 * sendNativeMessage communicate with client native app
 * Send a message accessing native app functions
 * @param msg The message
 * @param hostName The native application identifier
 */

function sendNativeMessage(msg, hostName) {
    if(!port){
        connect(hostName);
    }
    //msg = prepareMsg(msg);
    sendWebMessage({log:{sent:msg, to:hostName}});
    port.postMessage(msg);
    //chrome.runtime.sendNativeMessage(hostName, JSON.stringify(msg));
    sendWebMessage({log:{sent:msg}});
}

/**
 * Listener for native app messages
 * @param message The native app output
 */
function onNativeMessage(message) {
    if(message["printer"]){
        sendWebMessage(message);
        sendWebMessage({log:'adding printer: '+message["printer"]});
    }else if(message["log"]){
        sendWebMessage(message);
        if(message["log"].indexOf('print Job done') != -1){
            sendWebMessage({done:'reload'});
        }
    }else{
         sendWebMessage({log:'unexpected: '+message});
    }
}

/**
 * Listener for port disconnection fired
 * when connection closes or a error occurs
 * reset port to null
 */
function onDisconnected() {
  if(chrome.runtime.lastError.message.indexOf("not found") > -1 ){
    sendWebMessage({install:installationFile()});
    sendWebMessage({log:"host not installed"});
  }else if(chrome.runtime.lastError.message.indexOf("not installed") > -1 ){
    sendWebMessage({log:"host installation error"});
    sendWebMessage({error:"Installation error"});
  }else if(chrome.runtime.lastError.message.indexOf("forbidden") > -1 ){
    sendWebMessage({log:"host installation error"});
    sendWebMessage({error:"Configuration error"});
  }else if(chrome.runtime.lastError.message != ""){
    sendWebMessage({log:chrome.runtime.lastError.message});
  }
  port = null;
}

function installationFile(){
    if (navigator.appVersion.indexOf("Win")!=-1) {
        return "assets/BlueFocus_Printer.exe";
    }
    if ((navigator.appVersion.indexOf("Mac")!=-1) || (navigator.appVersion.indexOf("X11")!=-1) || (navigator.appVersion.indexOf("Linux")!=-1)){
        return "assets/BlueFocus_Printer.sh";
    }
    if (navigator.appVersion.indexOf("Unknown OS") != -1) {
            return 'choose:["linux":"assets/BlueFocus_Printer.sh","windows":"assets/BlueFocus_Printer.exe"]';
    }
}
/**
 * Create a native host connection using the host identifier
 * set listeners for messages and disconnection
 * @param hostName native host identifier
 */
function connect(hostName) {
  sendWebMessage({log:"Connecting to " + hostName});
  port = chrome.runtime.connectNative(hostName);
  port.onMessage.addListener(onNativeMessage);
  port.onDisconnect.addListener(onDisconnected);
}
/*******End Native connection handlers**********/

/*******Begin web connection handlers**********/
function sendWebMessage(msg){
    chrome.tabs.query({'active': true},function(tabs){
           chrome.tabs.sendMessage(tabs[0].id, msg);
    });
}

chrome.runtime.onMessage.addListener(
  /**
   * Runtime message receiver
   * @param request message data in JSON format
   *    Keys:
   *        list -> request for print list
   *        printer -> name of selected printer
   *        file -> url of the zip file to print
   *        log -> request a console.log on main window
   *        close -> request the disconnection from the host
   */
  function(request) {
    sendWebMessage({log:request});
  if(request.list){
    sendWebMessage({log:'Data sent to native host'});
    sendNativeMessage(request, nativeHost);
  }else if(request.printer){
     sendWebMessage({log:'Data sent to printer', data:request});
     sendNativeMessage(request, nativeHost);
     sendWebMessage({log:'Data sent to printer', data:request});
  }else if(request.log){
     sendWebMessage({log:'Data sent to printer', data:request});
  }else if(request.close){
     port.disconnect();
     port = null;
     sendWebMessage({log:'Host connection closed'});
  }
});
/*******End Web connection handlers**********/
