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

        var text = document.createElement("P");
		if(reviews[i].Comment)
		{
			text.innerHTML = "Review by " + reviews[i].UserID + '<br><b>' + reviews[i].Comment + '</b><br><b>Rating ' + reviews[i].Rating + "/5</b>";
        }
		else
		{
			text.innerHTML = "Review by " + reviews[i].UserID + '<br><br><b>Rating ' + reviews[i].Rating + "/5</b>";
		}
		row.appendChild(text);

        table.appendChild(row);
    }
}