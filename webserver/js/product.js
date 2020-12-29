async function loadReviews()
{
        loadFromServer();
}

async function loadFromServer()
{
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =  function()
    {
        if(this.readyState == 4 && this.status == 200)
        {
            var response = this.responseText;
            if(response != "")
            {
                var reviews = JSON.parse(response);
                generateHTML(reviews);
            }

        }
    }
    xhttp.open("GET", "/loadReviews", true);
    xhttp.send();
}

function generateHTML(reviewlist)
{
	var reviews = reviewlist.reviews;
    var table = document.getElementById("reviewArea");
    var i;
    for(i in reviews)
    {
        var row = document.createElement("DIV");
        row.className = "review";

        /*var image = document.createElement("AMP-IMG");
        image.setAttribute("height", "9");
        image.setAttribute("width", "16");
        image.setAttribute("src", products[i].path);
        image.setAttribute("layout", "responsive");
        image.setAttribute("class", "fixedsizedItem");
        row.appendChild(image)*/

        var text = document.createElement("P");
        text.innerHTML = "By " + reviews[i].UserID + "<br>" + reviews[i].Comment + "<br>"+ reviews[i].Rating;
        text.setAttribute("class","item");
        row.appendChild(text);

        table.appendChild(row);
    }
}