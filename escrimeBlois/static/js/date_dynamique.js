document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("date-naissance").oninput = function () {
    const inputValue = document.getElementById("date-naissance").value;
    fetch("/date_dynamique", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date_naissance: inputValue }),
    }).then((response) => response.json());
  };
});
