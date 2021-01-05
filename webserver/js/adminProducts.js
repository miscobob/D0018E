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
    table.innerHTML = "";
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
		text.innerHTML += '<br>Price: ' + products[i].price + '<br>Stock: ' + products[i].stock;
        text.setAttribute("class","item");
        row.appendChild(text);

        table.appendChild(row);
    }
}


function addProduct()
{
    var xhttp = new XMLHttpRequest();
    var form = document.getElementById("newproduct");
    var name = form.elements.name;
    var make = form.elements.make;
    var price = form.elements.price;
    var stock = form.elements.stock;
    xhttp.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200)
        {
            var response = xhttp.responseText;
            document.getElementById("response").innerHTML = response;
            form.reset();
            loadFromServer();
        }
    }
    if (name == "")
    {
        alert("Please give name");
        return;
    }
    if (make == "")
    {
        alert("Please give name");
        return;
    }
    xhttp.open('POST', "/admin/addProduct" ,true);
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    var data = "{\"name\":\""+name.value+"\",\"make\":\""+make.value
                +"\",\"price\":\""+price.value+"\",\"stock\":\""+stock.value+"\"}";
    xhttp.send(data);

    
}