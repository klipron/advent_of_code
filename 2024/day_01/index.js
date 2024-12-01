function solve() {
  /** @type {HTMLInputElement} */
  const filePicker = document.getElementById("file-picker");
  if (!filePicker.files.length) {
    alert("Please select a file first.");
    return;
  }
  const reader = new FileReader();
  reader.readAsText(filePicker.files[0]);
  reader.onload = function (evt) {
    /** @type {string} */
    const contents = evt.target.result;
    const lines = contents
      .split("\n")
      .filter((e) => e)
      .map((e) =>
        e
          .trim()
          .split(" ")
          .filter((e) => e.length)
          .map((e) => parseInt(e))
      );

    // const right = [];
    // for (const item of lines) {
    //   left.push(item[0]);
    //   right.push(item[1]);
    // }
    // left.sort();
    // right.sort();

    // const [left, right] = lines
    //   .reduce(
    //     (acc, val) => {
    //       acc[0].push(val[0]);
    //       acc[1].push(val[1]);
    //       return acc;
    //     },
    //     [[], []]
    //   )
    //   .map((e) => e.sort());

    const left = lines.map((e) => e[0]).sort();
    const right = lines.map((e) => e[1]).sort();

    const part1 = left.reduce(
      (acc, val, idx) => acc + Math.abs(val - right[idx]),
      0
    );
    document.getElementById("part1").innerHTML = `Answer Part 1: ${part1}`;

    /** @type {Map<int, int>} */
    const map = new Map();
    const counter = right.reduce(
      (acc, val) => acc.set(val, (acc.get(val) || 0) + 1),
      map
    );
    const part2 = left.reduce(
      (acc, val) => acc + val * (counter.get(val) || 0),
      0
    );
    document.getElementById("part2").innerHTML = `Answer Part 2: ${part2}`;
  };
}
