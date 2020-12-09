async function loadProducts()
{
        loadFromServer();
        generateHTML(basket);
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
                var basket = JSON.parse(response);
                generateHTML(basket);
            }

        }
    }
    xhttp.open("GET", "/loadProducts", true);
    xhttp.send();
}

function generateHTML(products)
{
    var table = document.getElementById("productsArea");
    var i;
    for(i in products)
    {
        var row = document.createElement("DIV");
        row.className = "product";

        var image = document.createElement("AMP-IMG");
        image.setAttribute("height", "9");
        image.setAttribute("width", "16");
        image.setAttribute("src", products[i].path);
        image.setAttribute("layout", "responsive");
        image.setAttribute("class", "fixedsizedItem");
        row.appendChild(image)

        var text = document.createElement("P");
        text.innerHTML = '<a href ="/products/'+products[i].pid+'">' + products[i].name + "</a> by "+ products>
        text.setAttribute("class","item");
        row.appendChild(text);

        /*var increaseCount = document.createElement("BUTTON");
        increaseCount.setAttribute("type","button");
        increaseCount.setAttribute("onclick","increaseCount("+products[i].pid+")");
        increaseCount.innerHTML = "+"
        increaseCount.setAttribute("class","fixedsizedItem");
        row.appendChild(increaseCount);*/

        table.appendChild(row);
    }
}

async function addItem(pid)
{

}

async function reduceCount(pid)
{

}

async function increaseCount(pid)
{

}

async function removeItem(pid)
{

}
