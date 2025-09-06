// static/js/script.js
// Placeholder for UI interactivity and input validation
// Example: Validate date range

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      // Date range validation
      const start = document.getElementById("start_date").value;
      const end = document.getElementById("end_date").value;
      if (
        !/^\d{4}-\d{2}-\d{2}$/.test(start) ||
        !/^\d{4}-\d{2}-\d{2}$/.test(end)
      ) {
        alert("Date format must be YYYY-MM-DD.");
        e.preventDefault();
        return;
      }
      if (start > end) {
        alert("Start date must be before end date.");
        e.preventDefault();
        return;
      }
      // Portfolio weights validation
      const weightFields = [
        document.getElementById("weight1"),
        document.getElementById("weight2"),
        document.getElementById("weight3"),
      ];
      let totalWeight = 0;
      for (let w of weightFields) {
        const val = parseFloat(w.value);
        if (isNaN(val) || val < 0 || val > 1) {
          alert("Weights must be numbers between 0 and 1.");
          e.preventDefault();
          return;
        }
        totalWeight += val;
      }
      if (Math.abs(totalWeight - 1.0) > 0.0001) {
        alert("Portfolio weights must sum to 1.0.");
        e.preventDefault();
        return;
      }
      // (Backend) Data sorting and date as index will be handled in Python, not JS
    });
  }
});
