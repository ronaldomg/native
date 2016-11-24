var iframe;
var printerList = [];
var loaded = false;
document.addEventListener("DOMNodeInserted", function (ev) {

	iframe = document.getElementById("gxp0_ifrm");
	if (iframe){
		document.getElementById("gxp0_ifrm").onload = function(){
			if(iframe.src.indexOf('himprimeviaapplet') > -1){
				listPrinters = "printers";

				var btn = iframe.contentWindow.document.getElementsByClassName("SpecialButtons");
				iframe.contentWindow.document.getElementById("LISTPRINTERContainer").style.display = 'none';
				iframe.contentWindow.document.getElementById("PRINTAPPLETContainer").style.display = 'none';
				chrome.runtime.sendMessage({list: listPrinters});
				var baseURL = window.location.href.split('/servlet/')[0];
				if (!loaded){
				    iframe.contentWindow.document.forms[0].vPORTA.innerHTML = "";
				    iframe.contentWindow.document.forms[0].vPORTA.parentNode.innerHTML += '<img id="bfpldrimg" src="'+baseURL+'/static/Resources/indicator.gif"/>';
                }
				for(i=0;i<btn.length;i++){
					if (btn[i].name == 'BTNIMPRIMIR'){
						btn[i].addEventListener("click", function(event){
							event = event || window.event;
							console.log(event);
							bfPrint(event);
						});
					}
				}
			}
		};
	}
}, false);
chrome.runtime.onMessage.addListener(function(request, sender) {
    if (request.log){
		console.log(request.log);
    }else if(request.printer){
        console.log(request.printer);
        addPrinter(request.printer);
		delAlert();
    }else if (request.done){
        chrome.runtime.sendMessage({close: 'connection'});
        //chrome.runtime.sendMessage({list: 'listPrinters'});
    }else if (request.error){ // TODO: Check if there is a way to improve error handling
        console.log(request.error);
    }else if (request.install){
        if (request.install != 'choose'){
			if(!document.getElementById("helperDowload")){
			    uri = chrome.extension.getURL(request.install);
				document.body.innerHTML += '<iframe id="helperDowload" width="1" height="1" frameborder="0" src=""></iframe>';
		        document.body.innerHTML += '<div id="downloadPopOver" class="PObutton">&Eacute; necess&aacute;rio baixar o assistente de impressão BlueFocus para continuar. <a href="#" onclick="javascript:document.getElementById(\'helperDowload\').src=(\''+uri+'\');document.getElementById(\'downloadPopOver\').style.display=\'none\';">Baixar</a></div>';
			}
        }
    }else if(request.download){
		delAlert();
        window.location.assign(chrome.extension.getURL(request.download));
    }
});

function getfile(file){
        uri = chrome.extension.getURL(file);
        document.innerHTML += '<iframe width="1" height="1" frameborder="0" src="'+uri+'"></iframe>';
        document.getElementById('downloadPopOver').style.display='none';
}

function addPrinter(printer){
	if(loaded){
	    iframe.contentWindow.document.getElementById("bfpldrimg").style.display = 'none';
	}
	loaded = true;
    var select = iframe.contentWindow.document.forms[0].vPORTA;
    var opt = document.createElement('option');
    printerList.push(printer);
    opt.value = printer;
    opt.innerHTML = printer;
    select.appendChild(opt);
}

function bfPrint(evt){
	iframe.contentWindow.document.getElementById("LISTPRINTERContainer").style.display = 'none';
	iframe.contentWindow.document.getElementById("PRINTAPPLETContainer").style.display = 'none';
	var cForm = evt.currentTarget.form;
    var selectedPrinter = evt.currentTarget.form.vPORTA.value;
    var zippedFile = getBaseUrl(cForm.vARQUIVO.value+'.zip');
    chrome.runtime.sendMessage({"file": zippedFile, "printer": selectedPrinter});
}

function verifyPrinter(form, printer){// f = form p = printer
    printers = form.vIMPRESSORANOME.options;
    for(i=0;i<printers.length;i++){
        if(printers[i].value == printer){
            console.log('ok');
            return true;
        }
    }
    return false;
}

function getBaseUrl(file){//TODO verify if is possible to change the file at genexus to provide the correct path
    if (file.indexOf("webapps\/") > -1){
        file = file.split("webapps")[1];
    }
    startPath = file.split("\/");
    loc = window.location.href;
    ret = loc.split("/"+startPath[1])[0]+file;
    return ret;
}

function delAlert(){
	el = document.getElementById("helperDowload");
	el.parentNode.removeChild(el);
}
