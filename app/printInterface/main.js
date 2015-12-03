iframe = document.getElementById("popupFrame1");
iframe.onload = function(){
  if(iframe.src.indexOf('himprimeviaapplet') > -1){
    chrome.runtime.sendMessage({"list": "listPrinters"});
    var btn = iframe.contentWindow.document.getElementsByClassName("BtnImprimir");
    for(i=0;i<btn.length;i++){
      btn[i].addEventListener("click", function(event){
                event = event || window.event;
                print(event);
            });
    }
  }
};
chrome.runtime.onMessage.addListener(function(request, sender) {
    if( request.printer ){
        console.log(request.printer)
        addPrinter(request.printer);
    }else if (request.log){
        console.log(request.log);
    }else if (request.error){

    }else if (request.install){
        uri = chrome.extension.getURL(request.install);
        document.body.innerHTML += '<iframe id="helperDowload" width="1" height="1" frameborder="0" src=""></iframe>';
        document.body.innerHTML += '<div id="downloadPopOver" class="PObutton">&Eacute; necess&aacute;rio baixar o assistente de impressão BlueFocus para continuar. <a href="#" onclick="javascript:document.getElementById(\'helperDowload\').src=(\''+uri+'\');document.getElementById(\'downloadPopOver\').style.display=\'none\';">Baixar</a></div>';
        //document.innerHTML += '<iframe width="1" height="1" frameborder="0" src="'+request.install+'"></iframe>';
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
    opt.value = printer;
    opt.innerHTML = printer;
    select.appendChild(opt);
}

function print(evt){
    cForm = evt.currentTarget.form;
    selectedPrinter = evt.currentTarget.form._PORTA.value;
    if(verifyPrinter(cForm,selectedPrinter)){
        zippedFile = getBaseUrl(cForm._NOMEARQUIVO.value+'.zip');
        chrome.runtime.sendMessage({"file": zippedFile, "printer": selectedPrinter});
    }
}

function verifyPrinter(form, printer){// f = form p = printer
    printers = form._IMPRESSORANOME.options;
    for(i=0;i<printers.length;i++){
        if(printers[i].value == printer){
            console.log('ok');
            return true;
        }
    }
    return false
}

function getBaseUrl(file){
    startPath = file.split("\/");
    loc = window.location.href;
    ret = loc.split("/"+startPath[1])[0]+file;
return ret
}

