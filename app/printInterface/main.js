var iframe = document.getElementById("popupFrame1");
var printerList = [];
if(iframe){
    iframe.onload = function(){
      if(iframe.src.indexOf('himprimeviaapplet') > -1){
        listPrinters = "printers";
        chrome.runtime.sendMessage({list: listPrinters});
        var btn = iframe.contentWindow.document.getElementsByClassName("BtnImprimir");
        for(i=0;i<btn.length;i++){
          btn[i].addEventListener("click", function(event){
                    event = event || window.event;
                    print(event);
                });
        }
      }
    };
}

chrome.runtime.onMessage.addListener(function(request, sender) {
    if (request.log){
        console.log(request.log);
    }else if( request.printer ){
        console.log(request.printer);
        addPrinter(request.printer);
    }else if (request.done){
        chrome.runtime.sendMessage({close: 'connection'});
        chrome.runtime.sendMessage({list: 'listPrinters'});
    }else if (request.error){ // TODO: Check if there is a way to improve error handling
        console.log(request.error);
    }else if (request.install){
        if (request.install != 'choose'){
            uri = chrome.extension.getURL(request.install);
            document.body.innerHTML += '<iframe id="helperDowload" width="1" height="1" frameborder="0" src=""></iframe>';
            document.body.innerHTML += '<div id="downloadPopOver" class="PObutton">&Eacute; necess&aacute;rio baixar o assistente de impressão BlueFocus para continuar. <a href="#" onclick="javascript:document.getElementById(\'helperDowload\').src=(\''+uri+'\');document.getElementById(\'downloadPopOver\').style.display=\'none\';">Baixar</a></div>';
        }
    }else if(request.download){
        window.location.assign(chrome.extension.getURL(request.download));
    }
});

function getfile(file){
        uri = chrome.extension.getURL(file);
        document.innerHTML += '<iframe width="1" height="1" frameborder="0" src="'+uri+'"></iframe>';
        document.getElementById('downloadPopOver').style.display='none';
}

function addPrinter(printer){
    var select = iframe.contentWindow.document.forms[0]._PORTA;
    var opt = document.createElement('option');
    printerList.push(printer);
    opt.value = printer;
    opt.innerHTML = printer;
    select.appendChild(opt);
}

function print(evt){
    cForm = evt.currentTarget.form;
    selectedPrinter = evt.currentTarget.form._PORTA.value;
    zippedFile = getBaseUrl(cForm._NOMEARQUIVO.value+'.zip');
    chrome.runtime.sendMessage({"file": zippedFile, "printer": selectedPrinter});
}

function verifyPrinter(form, printer){// f = form p = printer
    printers = form._IMPRESSORANOME.options;
    for(i=0;i<printers.length;i++){
        if(printers[i].value == printer){
            console.log('ok');
            return true;
        }
    }
    return false;
}

function getBaseUrl(file){
    startPath = file.split("\/");
    loc = window.location.href;
    ret = loc.split("/"+startPath[1])[0]+file;
    return ret;
}
