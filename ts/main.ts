type HTMLValuedElement = HTMLElement & { value: string, select: () => void } | null;

// Website Scroll Position
document.addEventListener("DOMContentLoaded", function (event) {
  let scrollpos = localStorage.getItem("scrollpos");
  if (scrollpos) window.scrollTo(0, parseInt(scrollpos));
});

window.onbeforeunload = function (e) {
  localStorage.setItem("scrollpos", `${window.scrollY}`);
};

// Website Themes
const themes = {
  purple: {
    primary: "#4c237e",
    secondary: "#2e154c",
    homeimage: "url(images/home_purple.svg)",
  },
  orange: {
    primary: "#d3671d",
    secondary: "#7f3e11",
    homeimage: "url(images/home_orange.svg)",
  },
  yellow: {
    primary: "#e0b12d",
    secondary: "#8d6d15",
    homeimage: "url(images/home_yellow.svg)",
  },
  brown: {
    primary: "#a16b4c",
    secondary: "#61402e",
    homeimage: "url(images/home_brown.svg)",
  },
  black: {
    primary: "#3b363f",
    secondary: "#232026",
    homeimage: "url(images/home_black.svg)",
  },
  green: {
    primary: "#249465",
    secondary: "#16593d",
    homeimage: "url(images/home_green.svg)",
  },
  pink: {
    primary: "#fa4664",
    secondary: "#bb0523",
    homeimage: "url(images/home_pink.svg)",
  },
  blue: {
    primary: "#2575aa",
    secondary: "#164666",
    homeimage: "url(images/home_blue.svg)",
  },
  red: {
    primary: "#c95252",
    secondary: "#812828",
    homeimage: "url(images/home_red.svg)",
  },
};

type Theme = keyof typeof themes;
type ThemeData = typeof themes[Theme];

$(document).on("change", "#theme", function () {
  const theme = $("#theme").val() as Theme;
  localStorage.setItem("theme", theme);
  loadTheme();
});

function loadTheme() {
  const theme = localStorage.getItem("theme") as Theme;
  if (!theme) return;
  const root = document.querySelector(":root") as HTMLBodyElement;
  root.style.setProperty("--primary", themes[theme]["primary"]);
  root.style.setProperty("--secondary", themes[theme]["secondary"]);
  root.style.setProperty("--homeimage", themes[theme]["homeimage"]);
}
loadTheme();

document.addEventListener("DOMContentLoaded", function () {
  const theme = localStorage.getItem("theme") as Theme | null ?? "pink";
  ($("#theme") as unknown as HTMLElement & { selectpicker: (val: string, theme: keyof typeof themes) => void }).selectpicker("val", theme);
});

// Form JS Buttons
function eraseInputText(targetelement: string) {
  const target = document.getElementById(targetelement) as HTMLValuedElement;
  if (target) target.value = "";
}

function moveToInput() {
  const outputTextElement = document.getElementById("outputtext") as HTMLValuedElement;
  const inputTextElement = document.getElementById("inputtext") as HTMLValuedElement;
  if (outputTextElement && inputTextElement) {
    const text = outputTextElement.value;
    inputTextElement.value = text;
  }
}

function copyToClipboard() {
  const textarea = document.getElementById("outputtext") as HTMLValuedElement;
  if (!textarea) return;
  textarea.select();
  document.execCommand("copy");
}

const range = (end: number, start = 0, step = 1) => {
  const keys = new Array(end).keys();
  return Array.from(keys).slice(start).map(val => val * step);
}

function switchInputFields(setA: string[], setB: string[]) {
  for (const i of range(setA.length)) {
    const fielda = document.getElementById(setA[i]) as HTMLValuedElement;
    const fieldb = document.getElementById(setB[i]) as HTMLValuedElement;
    if (!fielda || !fieldb) break;
    const oldFieldAValue = fielda.value;
    fielda.value = fieldb.value;
    fieldb.value = oldFieldAValue;
  }
}

// Form Result Control
$(document).ready(function () {
  let buttonpressed: string | undefined;
  const type = $(".actiontype");
  const form = document.getElementById("calculationform") as HTMLFormElement | null;
  imageForm(document.getElementById("imageform") as unknown as HTMLFormElement);
  $(".submitbutton").click(function () {
    buttonpressed = $(this).attr("name");
  });
  if (form) form.onsubmit = async (e) => {
    e.preventDefault();

    type.attr("name", buttonpressed ?? null);
    const url = form.attributes.getNamedItem("action")?.textContent;

    if (!url) return;
    const targetFormInputElems = document.getElementsByClassName("form-control") as HTMLCollectionOf<Exclude<HTMLValuedElement, null>>;
    const targetFormInputs = Object.entries(targetFormInputElems).filter(([key, value]) => {
      try {
        const i = parseInt(key);
        return !isNaN(i);
      }
      catch {
        return false;
      }
    }).reduce((acc, [, value]) => ({ ...acc, [value.id]: value.value }), {} as Record<string, string>);

    const errorElem = $("[id*='error']");
    const helpElem = $("[id*='help']");

    // Clear errors
    errorElem.attr("style", "display: none;");
    errorElem.toArray().forEach(elem => { elem.innerText = ""; });

    const result = await fetch(url, {
      method: "POST", body: $("#calculationform").serialize(), headers: {
        "Content-Type":
          "application/x-www-form-urlencoded; charset=UTF-8"
      }
    });

    if (result.ok) {
      const data = await result.json();
      if (typeof data == "object" && data.error) {
        delete data.error;
        // Assign each error to the appropriate field
        errorElem.toArray().forEach(element => {
          const fieldName = /.*(?=error)/.exec(element.id)?.[0] ?? "";
          if (typeof data[fieldName] === "string") element.innerText = data[fieldName];
        });
        errorElem.removeAttr("style");
        helpElem.attr("style", "display: none;")
        return;
      }
      // Display the result
      const outputtext = $("#outputtext");
      if (data instanceof Array) {
        outputtext.val(data.join("|"));
      } else if (typeof data === "object") {
        outputtext.val(Object
          .entries(data)
          .map(([key, value]) =>
            `key: ${key}, value: ${value}`)
          .join("|"));
      } else {
        outputtext.val(`${data}`);
      }
      $("[id*='help']").removeAttr("style");
      const resultcard = $(".resultcard");
      resultcard.removeAttr("style");
      if (data !== "Process Execution Failed")
        outputtext.removeClass("text-danger");
      else {
        outputtext.addClass("text-danger");
        errorElem.removeAttr("style");
      }
    }
  }
});

/**
 * @param file The file object that should be serialised
 * @returns A promise of a base64 string
 */
const serialiseFile = async (file: File): Promise<string> => 
  new Uint8Array(await file.arrayBuffer()).reduce((acc, curr) => 
    acc.concat(String.fromCharCode(curr))
  , "");

/**
 * Configures the submission of an imageform element
 * @param form A selected image form element
 */
const imageForm = (form: HTMLFormElement) => {
  form.onsubmit = (async submission => {
    submission.preventDefault();
    const target = submission.target as unknown as HTMLFormElement;
    const inputs = Object.values(target.getElementsByClassName("sendableinput")) as unknown as HTMLInputElement[];
    const selectedFiles: (File | null)[] = inputs.filter(input => input.className.includes("imageinput")).map(
      imageInput => imageInput.files?.item(0) ?? null).flat(1);
    const formData = {images: await Promise.all(selectedFiles.map(async file => file ? await serialiseFile(file) : null)),
      alpha: inputs[0].value
    }
    const result = await fetch("", {method: "POST", body: JSON.stringify(formData)});
    if (result.ok) {
      
    }
    else {

    }
  });
}