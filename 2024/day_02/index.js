/** @type {HTMLInputElement} */
const filePicker = document.getElementById("file-picker");

/** @type {HTMLDivElement} */
const answers = document.getElementById("answers");

const year = 2024;
const day = 2;

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
  const lines = fileContents
    .split("\n")
    .filter((e) => e)
    .map((e) =>
      e
        .trim()
        .split(" ")
        .map((e) => parseInt(e))
    );

  /**
   *
   * @param {number[]} levels
   * @returns
   */
  function isSafe(levels) {
    const diffs = levels.slice(0, -1).map((num, idx) => levels[idx + 1] - num);
    const lt = diffs.reduce((acc, val) => acc && val < 0, true);
    const gt = diffs.reduce((acc, val) => acc && val > 0, true);
    if (!(lt || gt)) {
      return false;
    }
    if (diffs.filter((num) => Math.abs(num) > 3).length) {
      return false;
    }
    return true;
  }

  let safe = 0;
  let unsafeIgnore = 0;
  for (const levels of lines) {
    if (isSafe(levels)) {
      safe += 1;
      continue;
    }
    for (const idx in levels) {
      if (isSafe(levels.filter((_, i) => idx != i))) {
        unsafeIgnore += 1;
        break;
      }
    }
  }
  showAnswer({ part: 1, value: safe });
  showAnswer({ part: 2, value: safe + unsafeIgnore });
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
