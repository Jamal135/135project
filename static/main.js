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

$(document).on("change", "#theme", function () {
  let theme = $("#theme").val();
  localStorage.setItem("theme", theme);
  loadTheme();
});

function loadTheme() {
  const theme = localStorage.getItem("theme");
  if (!theme) return;
  const root = document.querySelector(":root");
  root.style.setProperty("--primary", themes[theme]["primary"]);
  root.style.setProperty("--secondary", themes[theme]["secondary"]);
  root.style.setProperty("--homeimage", themes[theme]["homeimage"]);
}
loadTheme();

document.addEventListener("DOMContentLoaded", function () {
  let theme = localStorage.getItem("theme");
  if (!theme) theme = "pink";
  $("#theme").selectpicker("val", theme);
});

// Form JS Buttons
function eraseInputText(targetelement) {
  document.getElementById( targetelement ).value = "";
}

function moveToInput() {
  var text = document.getElementById("outputtext").value;
  document.getElementById("inputtext").value = text;
}

function copyToClipboard() {
  let textarea = document.getElementById("outputtext");
  textarea.select();
  document.execCommand("copy");
} 

function switchInputFields(setA, setB) {
  for (const [i] of setA.entries()) {
    const fielda = document.getElementById(setA[i]).value
    const fieldb = document.getElementById(setB[i]).value;
    document.getElementById(setA[i]).value = fieldb
    document.getElementById(setB[i]).value = fielda
  }
}

// Form Result Control
$(document).ready(function () {
  var buttonpressed;
  $(".submitbutton").click(function () {
    buttonpressed = $(this).attr("name");
  });
  $("#calculationform").submit(function (e) {
    e.preventDefault();
    var type = $(".actiontype");
    type.attr("name", buttonpressed);
    var form = $(this);
    var url = form.attr("action");
    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(),
      success: function (data) {
        var resultcard = $(".resultcard");
        $("[id*='help']").removeAttr("style", "display: none;");
        $("[id*='error']").attr("style", "display: none;");
        if (data.constructor == Object) {
          resultcard.attr("style", "display: none;");
          for (const property in data) {
            document
              .getElementById(`${property}help`)
              .setAttribute("style", "display: none;");
            const errorelement = document.getElementById(`${property}error`);
            errorelement.removeAttribute("style", "display: none;");
            errorelement.textContent = data[property];
          }
        } else {
          var outputtext = $("#outputtext");
          outputtext.val(data);
          outputtext.removeClass("text-danger");
          if (data === "Process Execution Failed") {
            outputtext.addClass("text-danger");
          }
          resultcard.removeAttr("style");
        }
      },
    });
  });
});
