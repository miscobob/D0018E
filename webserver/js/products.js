async function loadProducts()
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
                var products = JSON.parse(response);
                generateHTML(products);
            }

        }
    }
    xhttp.open("GET", "/loadProducts", true);
    xhttp.send();
}

function generateHTML(productlist)
{
	var products = productlist.products;
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
        text.innerHTML = '<a href ="/products/'+products[i].pid+'">' + products[i].name + "</a> by "+ products[i].make;
        text.setAttribute("class","item");
        row.appendChild(text);

        var addToCartButton = document.createElement("BUTTON");
        addToCartButton.setAttribute("type","button");
        addToCartButton.setAttribute("onclick","addToCart("+products[i].pid+")");
        addToCartButton.innerHTML = "Add to cart"
        addToCartButton.setAttribute("class","fixedsizedItem");
        row.appendChild(addToCartButton);

        table.appendChild(row);
    }
}

async function addToCart(pid)
{
    increaseCount(pid);
}
