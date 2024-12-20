/** @type {HTMLInputElement} */
const filePicker = document.getElementById("file-picker");

/** @type {HTMLDivElement} */
const answers = document.getElementById("answers");

const year = 2024;
const day = 3;

for (const tag of ["title", "h1"]) {
  document.querySelector(tag).innerHTML = `Advent of Code ${year} Day ${day}`;
}

/**
 *
 * @param {{part: string, value: number}} answer
 */
function showAnswer(answer) {
  const div = document.createElement("div");
  const p = document.createElement("p");
  p.innerHTML = `Answer Part ${answer.part}: ${answer.value}`;
  div.append(p);
  answers.append(div);
}

/**
 *
 * @param {string} fileContents
 */
function solve(fileContents) {
  let enabled = true;
  let total = 0;
  let enabledTotal = 0;
  Array.from(
    fileContents.matchAll(/mul\((\d+),(\d+)\)|do\(\)|don't\(\)/g)
  ).forEach((val) => {
    if (val[0] == "do()") {
      enabled = true;
    } else if (val[0] == "don't()") {
      enabled = false;
    } else {
      const value = parseInt(val[1] || 0) * parseInt(val[2] || 0);
      total += value;
      enabledTotal += enabled ? value : 0;
    }
  }, 0);
  showAnswer({ part: 1, value: total });
  showAnswer({ part: 2, value: enabledTotal });
}

filePicker.addEventListener("change", () => {
  answers.innerHTML = "";
  if (!filePicker.files.length) {
    alert("Please select a file first.");
    return;
  }
  const reader = new FileReader();
  reader.readAsText(filePicker.files[0]);
  reader.onload = (evt) => solve(evt.target.result);
});
