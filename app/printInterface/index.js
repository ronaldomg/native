document.getElementById("windows").addEventListener("click", function()
    {
        chrome.tabs.query
        (
            {'active': true},function(tabs)
            {
                chrome.tabs.sendMessage
                (
                    tabs[0].id, {download:'assets/BlueFocus_Printer.exe'}
                );
            }
        );
    }
);
document.getElementById("nix").addEventListener
("click", function()
    {
        chrome.tabs.query
        (
            {'active': true},function(tabs)
            {
                chrome.tabs.sendMessage
                (
                    tabs[0].id, {download:'assets/BlueFocus_Printer.sh'}
                );
            }
        );
    }
);