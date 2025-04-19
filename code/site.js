
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

function formatTable(content = []) {

	function formatElement(element) {
		// {"name": "Green LED", "id": 15, "io_type": "OUT"},
		if (element.io_type == "IN") {
			return "<div class='output'>" + element.name + "</div>"
		} else if (element.io_type == "OUT") {
			return "<div class='input-type'>"
				+ element.name
				+ "<div>"
				+ "<div>    <button type='button' onClick='pressButton('" + element.id + "','on')'>On!</button></div>\n"
				+ "<div>    <button type='button' onClick='pressButton('" + element.id + "','toggle')'>Toggle!</button></div>\n"
				+ "<div>    <button type='button' onClick='pressButton('" + element.id + "','off')'>Off!</button></div>\n"
				+ "</div>\n</div>\n"
		} else {
			return "";
		}
	}

	return content.map(formatElement).reduce((a, b) => a + b, "");
}

function updateTable() {
	fetch("/data.json", {
		method: "GET",
	})
		.then(r => r.json())
		.then(data => {

			console.log(data);
			content = formatTable(data);
			console.log(content);
			document.getElementById("mainContent").innerHTML = content;
		})
}

interval = setInterval(updateTable, 5000)