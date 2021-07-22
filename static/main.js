document.addEventListener("DOMContentLoaded", function(event) { 
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);
    });

window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};

function eraseInputText() {
    document.getElementById("inputtext").value = "";
};

function moveToInput() {
    var text = document.getElementById("outputtext").value;
    document.getElementById("inputtext").value = text;
};

function copyToClipboard() {
    var element = document.getElementById("outputtext");
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
};
