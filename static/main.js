// Website Scroll Position
document.addEventListener("DOMContentLoaded", function (event) {
  var scrollpos = localStorage.getItem("scrollpos");
  if (scrollpos) window.scrollTo(0, scrollpos);
});

window.onbeforeunload = function (e) {
  localStorage.setItem("scrollpos", window.scrollY);
};

// Website Themes
var themes = {
  purple: {
    primary: "#4c237e",
    secondary: "#2e154c",
    homeimage: "url(images/home_purple.png",
  },
  orange: {
    primary: "#d3671d",
    secondary: "#7f3e11",
    homeimage: "url(images/home_orange.png)",
  },
  yellow: {
    primary: "#e0b12d",
    secondary: "#8d6d15",
    homeimage: "url(images/home_yellow.png)",
  },
  brown: {
    primary: "#a16b4c",
    secondary: "#61402e",
    homeimage: "url(images/home_brown.png)",
  },
  black: {
    primary: "#3b363f",
    secondary: "#232026",
    homeimage: "url(images/home_black.png)",
  },
  green: {
    primary: "#249465",
    secondary: "#16593d",
    homeimage: "url(images/home_green.png)",
  },
  pink: {
    primary: "#fa4664",
    secondary: "#bb0523",
    homeimage: "url(images/home_pink.png)",
  },
  blue: {
    primary: "#2575aa",
    secondary: "#164666",
    homeimage: "url(images/home_blue.png)",
  },
  red: {
    primary: "#c95252",
    secondary: "#812828",
    homeimage: "url(images/home_red.png)",
  },
};

$(document).on("change", "#theme", function() {
  let theme = $("#theme").val();
  localStorage.setItem("theme", theme)
  loadTheme();
})

function loadTheme() {
  const theme = localStorage.getItem("theme");
  if (!theme) return;
  const root = document.querySelector(":root");
  root.style.setProperty("--primary", themes[theme]["primary"]);
  root.style.setProperty("--secondary", themes[theme]["secondary"]);
  root.style.setProperty("--homeimage", themes[theme]["homeimage"]);
}
loadTheme();

document.addEventListener("DOMContentLoaded", function(){
  let theme = localStorage.getItem("theme")
  if (!theme) theme = "pink"
  $("#theme").selectpicker("val", theme);
});

// Form JS Buttons
function eraseInputText() {
  document.getElementById("inputtext").value = "";
}

function moveToInput() {
  var text = document.getElementById("outputtext").value;
  document.getElementById("inputtext").value = text;
}

function copyToClipboard() {
  var element = document.getElementById("outputtext");
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
}

// Form Image Controls
$(document).ready(function () {
  $(document).on("change", ".btn-file :file", function () {
    var input = $(this),
      label = input.val().replace(/\\/g, "/").replace(/.*\//, "");
    input.trigger("fileselect", [label]);
  });

  $(".btn-file :file").on("fileselect", function (event, label) {
    var input = $(this).parents(".input-group").find(":text"),
      log = label;

    if (input.length) {
      input.val(log);
    } else {
      if (log) alert(log);
    }
  });
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        $("#img-upload").attr("src", e.target.result);
      };

      reader.readAsDataURL(input.files[0]);
    }
  }

  $("#imgInp").change(function () {
    readURL(this);
    $("#removeImage").toggle(); // show remove link
  });

  $("#removeImage").click(function (e) {
    e.preventDefault(); // prevent default action of link
    $("#blah").attr("src", ""); //clear image src
    $("#imgInp").val(""); // clear image input value
    $("#removeImage").toggle(); // hide remove link.
  });
});
