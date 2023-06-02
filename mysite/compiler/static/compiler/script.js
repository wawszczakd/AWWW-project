var selectedFileId = null;

var selectedStandard = null;
var selectedOptimization = null;
var selectedProcessor = null;
var selectedDependent = null;

var dataDiv = document.getElementById("data-div");
var buttons = document.querySelectorAll(".trapezoid-button");

var compiled = false;

function ShowTab(tabName) {
	buttons.forEach(function(button) {
		if (button.id === tabName) {
			button.classList.add("clicked");
		} else {
			button.classList.remove("clicked");
		}
	});
	switch (tabName) {
	case "standard":
		dataDiv.innerHTML = `
		<form id="standard">
			<input type="radio" name="standard" value="c89" ${selectedStandard === "c89" ? "checked" : ""}>C89<br>
			<input type="radio" name="standard" value="c99" ${selectedStandard === "c99" ? "checked" : ""}>C99<br>
			<input type="radio" name="standard" value="c11" ${selectedStandard === "c11" ? "checked" : ""}>C11<br>
		</form>`;
		break;
	case "optimizations":
		dataDiv.innerHTML = `
		<form id="optimization">
			<input type="radio" name="optimization" value="gcse" ${selectedOptimization === "gcse" ? "checked" : ""}>gcse<br>
			<input type="radio" name="optimization" value="invariant" ${selectedOptimization === "invariant" ? "checked" : ""}>invariant<br>
			<input type="radio" name="optimization" value="induction" ${selectedOptimization === "induction" ? "checked" : ""}>induction<br>
			<input type="radio" name="optimization" value="loopreverse" ${selectedOptimization === "loopreverse" ? "checked" : ""}>loopreverse<br>
		</form>`;
		break;
	case "processor":
		dataDiv.innerHTML = `
		<form id="processor">
			<input type="radio" name="processor" value="mcs51" ${selectedProcessor === "mcs51" ? "checked" : ""}>mcs51<br>
			<input type="radio" name="processor" value="z80" ${selectedProcessor === "z80" ? "checked" : ""}>z80<br>
			<input type="radio" name="processor" value="stm8" ${selectedProcessor === "stm8" ? "checked" : ""}>stm8<br>
		</form>`;
		break;
	case "dependent":
		if (selectedProcessor == "mcs51") {
		dataDiv.innerHTML = `
			<form id="dependent">
			<input type="radio" name="dependent" value="small" ${selectedDependent === "small" ? "checked" : ""}>small<br>
			<input type="radio" name="dependent" value="medium" ${selectedDependent === "medium" ? "checked" : ""}>medium<br>
			<input type="radio" name="dependent" value="large" ${selectedDependent === "large" ? "checked" : ""}>large<br>
			</form>`;
		}
		else if (selectedProcessor == "z80") {
		dataDiv.innerHTML = `
			<form id="dependent">
			<input type="radio" name="dependent" value="rgbds" ${selectedDependent === "rgbds" ? "checked" : ""}>rgbds<br>
			<input type="radio" name="dependent" value="z80asm" ${selectedDependent === "z80asm" ? "checked" : ""}>z80asm<br>
			<input type="radio" name="dependent" value="isas" ${selectedDependent === "isas" ? "checked" : ""}>isas<br>
			</form>`;
		}
		else if (selectedProcessor == "stm8") {
		dataDiv.innerHTML = `
			<form id="dependent">
			<input type="radio" name="dependent" value="medium" ${selectedDependent === "medium" ? "checked" : ""}>medium<br>
			<input type="radio" name="dependent" value="large" ${selectedDependent === "large" ? "checked" : ""}>large<br>
			</form>`;
		}
		else {
			dataDiv.innerHTML = `<h3>Wybierz procesor</h3>`;
		}
		break;
	}
}

document.addEventListener("DOMContentLoaded", function(event) {
	var dataDiv = document.getElementById("data-div");
	dataDiv.addEventListener("change", function(event) {
		if (event.target.name === "standard") {
			selectedStandard = event.target.value;
		}
		else if (event.target.name === "optimization") {
			selectedOptimization = event.target.value;
		}
		else if (event.target.name === "processor") {
			selectedProcessor = event.target.value;
		}
		else if (event.target.name === "dependent") {
			selectedDependent = event.target.value;
		}
	});
});

function highlight(element) {
	element.classList.add("highlight");
	element.onmouseout = function() {
		element.classList.remove("highlight");
	}
}

function handleFileClick(fileId) {
	selectedFileId = fileId;
	
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status === 200) {
			document.getElementById('file-content').innerHTML = xhr.responseText;
		}
	};
	xhr.open('GET', '/main/file/' + fileId, true);
	xhr.send();
	
	compiled = false;
}

function handleCompilation() {
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
	  if (xhr.readyState === 4 && xhr.status === 200) {
		document.getElementById('code').innerHTML = xhr.responseText;
	  }
	};
	xhr.open('GET', '/main/file/' + selectedFileId + '/compiled/' + selectedStandard + '/' + selectedOptimization + '/' + selectedProcessor + '/' + selectedDependent + '/', true);
	xhr.send();
	
	selectedStandard = null;
	selectedOptimization = null;
	selectedProcessor = null;
	selectedDependent = null;
	
	dataDiv.innerHTML = `<h3>Wybierz opcje, klikając powyższe przyciski.</h3>`;
	
	buttons.forEach(function(button) {
		button.classList.remove("clicked");
	});
	
	compiled = true;
}

function downloadCompiledFile() {
	if (!compiled) {
		alert("Nie skompilowano pliku.");
		return;
	}
	
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status === 200) {
			var filename = xhr.getResponseHeader('Content-Disposition').match(/filename="(.+)"/)[1];
			var content = xhr.responseText;
			var element = document.createElement('a');
			element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
			element.setAttribute('download', filename);
			element.style.display = 'none';
			document.body.appendChild(element);
			element.click();
			document.body.removeChild(element);
		}
	};
	xhr.open('GET', '/main/compiled/download/', true);
	xhr.send();
}

function toggleSection(sectionId) {
	var section = document.getElementById("section" + sectionId);

	if (section.style.display === "none" || section.style.display === "") {
		section.style.display = "block";
	} else {
		section.style.display = "none";
	}
}