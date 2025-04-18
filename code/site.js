
window.addEventListener("DOMContentLoaded", function () {
	console.log("Window loaded.")
	updateTable();
}, false);

function pressButton(target, value) {
	fetch("", {
		method: "POST",
		body: JSON.stringify({
			//[target]: value,
			target: target,
			value: value,
		}),
		headers: {
			"Content-type": "application/json; charset=UTF-8"
		}
	}).then(r => { console.log(r) })
}

function formatTable(content = "") {
	return "TO BE IMPLEMENTED" + content
}

function updateTable() {
	fetch("/data.json", {
		method: "GET",
	})
		.then(r => r.json())
		.then(data => {

			console.log(data);
			content = formatTable(data);
			document.getElementById("mainContent").innerHTML = content;
		})
}

interval = setInterval(updateTable, 5000)