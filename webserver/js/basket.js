
async function loadBasket()
{
    const cachename = "basket";
    const TTL = 3600000
    var cache = localStorage.getItem(cachename);
    if(cache == null)
    {
        loadFromServer();
    }
    else
    {
        var basket = JSON.parse(cache);
        var dts = Date.parse(basket.dts);
        if(Date.now()-dts>TTL)
        {
            localStorage.removeItem(cachename); /// remove from storage 
            loadFromServer(); // updates with new data
        }
        else
        {
            generateHTML(basket);
        }
        
    }
}

async function loadFromServer()
{
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =  function()
    {
        const cachename = "basket";
        if(this.readyState == 4 && this.status == 200)
        {
            var response = this.responseText;
            if(response != "")
            {
                var basket = JSON.parse(response);
                localStorage.setItem(cachename,response);
                generateHTML(basket);
            }
            
        } 
    }
    xhttp.open("GET", "/loadBasket", true);
    xhttp.send();
}

function generateHTML(basket)
{
    var products = basket.products;
    var table = document.getElementById("basketArea");
    var i;
    for(i in products)
    {
        var row = document.createElement("DIV");
        row.className = "basketRow";
        
        var image = document.createElement("AMP-IMG");
        image.setAttribute("height","9");
		image.setAttribute("width","16");
		image.setAttribute("src",products[i].path);
        image.setAttribute("layout","responsive");
        image.setAttribute("class","fixedsizedItem");
        ///image.style.display = "table-cell";
        row.appendChild(image)
        
        var text = document.createElement("P");
        text.innerHTML = '<a href ="/product/'+products[i].pid+'">' + products[i].name + "</a> by "+ products[i].make + " in basket "+ products[i].count;
        ///text.style.display = "table-cell";
        text.setAttribute("class","basketItem");
        row.appendChild(text);

        var increaseCount = document.createElement("BUTTON");
        increaseCount.setAttribute("type","button");
        increaseCount.setAttribute("onclick","increaseCount("+products[i].pid+")");
        increaseCount.innerHTML = "+"
        ///increaseCount.style.display = "table-cell";
        increaseCount.setAttribute("class","fixedsizedItem");
        row.appendChild(increaseCount);

        var reduceCount = document.createElement("BUTTON");
        reduceCount.setAttribute("type","button");
        reduceCount.setAttribute("onclick","reduceCount("+products[i].pid+")");
        reduceCount.innerHTML = "-"
        ///reduceCount.style.display = "table-cell";
        reduceCount.setAttribute("class","fixedsizedItem");
        row.appendChild(reduceCount);
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