async function getNASA() {
    document.getElementById("title").innerHTML = "Loading...";

    try {

        const response = await fetch("/api/nasa");

        const data = await response.json();

        document.getElementById("title").innerHTML = data.title;
        document.getElementById("date").innerHTML = "Date: " + data.date;
        document.getElementById("image").src = data.url;
        document.getElementById("description").innerHTML = data.explanation;

    }

    catch(error){

        document.getElementById("title").innerHTML = "Error loading data.";

    }

}

window.onload = getNASA;