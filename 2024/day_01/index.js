/** @type {HTMLInputElement} */
const filePicker = document.getElementById("file-picker");

/** @type {HTMLDivElement} */
const answers = document.getElementById("answers");

const year = 2024;
const day = 1;

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
        .filter((e) => e.length)
        .map((e) => parseInt(e))
    );

  const left = lines.map((e) => e[0]).sort();
  const right = lines.map((e) => e[1]).sort();

  showAnswer({
    part: 1,
    value: left.reduce((acc, val, idx) => acc + Math.abs(val - right[idx]), 0),
  });

  /** @type {Map<int, int>} */
  const map = new Map();
  const counter = right.reduce(
    (acc, val) => acc.set(val, (acc.get(val) || 0) + 1),
    map
  );

  showAnswer({
    part: 2,
    value: left.reduce((acc, val) => acc + val * (counter.get(val) || 0), 0),
  });
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
