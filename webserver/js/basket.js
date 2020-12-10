
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
                var date = new Date();
                basket.dts = date.toISOString();
                localStorage.setItem(cachename, JSON.stringify(basket));
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
    console.log(products);
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
        text.innerHTML = '<a href ="/products/'+products[i].pid+'">' + products[i].name + "</a> by "+ products[i].make + " in basket "+ products[i].count;
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
        reduceCount.setAttribute("onclick","decreaseCount("+products[i].pid+")");
        reduceCount.innerHTML = "-"
        ///reduceCount.style.display = "table-cell";
        reduceCount.setAttribute("class","fixedsizedItem");
        row.appendChild(reduceCount);
        table.appendChild(row);
    }
}


async function increaseCount(pid)
{
    var cachename = "basket";
    var cache = localStorage.getItem(cachename);
    if(cache != null)
    {
        var basket = JSON.parse(cache);
        var products = basket.products;
        var i;
        for( i in products)
        {
            if(products[i].pid == pid)
            {
                products[i].count +=1;
                updateServer(pid, 1)
                localStorage.setItem(cachename, JSON.stringify(basket));
                return;
            }
        }
    }
    var basket = {};
    var products = [];
    var date = new Date();
    basket.products = products;
    basket.dts = date.toISOString();
    ///console.log(basket)
    requestJSON(basket, pid, 1);

}

async function decreaseCount(pid)
{
    var cachename = "basket";
    var cache = localStorage.getItem(cachename);
    if(cache != "")
    {
        var basket = JSON.parse(cache);
        var products = basket.products;
        var i;
        for( i in products)
        {
            if(products[i].pid == pid)
            {
                products[i].count -=1;
                if (products[i].count == 0)
                {
                    if (i == 0)
                        products.splice(0,1);
                    else
                        products.splice(i,i);
                }
                updateServer(pid, -1);
                localStorage.setItem(cachename, JSON.stringify(basket));
                return;
            }
        }
    }
    alert("Product not in basket");
}



function requestJSON(basket, pid, mod)
{
    var xhttp = new XMLHttpRequest();
    //console.log(basket)
    xhttp.onreadystatechange =  function()
    {
        if(this.readyState == 4 && this.status == 200)
        {
            var response = this.responseText;
            var e = document.createElement("P");
            e.innerHTML = response.toString();
            document.getElementById("body").appendChild(e);
            if(response == "" || response == null)
            {
                alert("You tried to add a non existing product!");
            }
            else
            {
                var jsobj = JSON.parse(response.toString());
                basket.products.push(jsobj);
                var cachename = "basket";
                console.log(basket)
                var cache = localStorage.setItem(cachename, JSON.stringify(basket));
            }
        }
    }
    xhttp.open("POST", "/addProductToBasket", true);
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    xhttp.send(JSON.stringify({"pid":pid, "mod":mod}));
}

function updateServer(pid, mod)
{
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/updateBasket", true);
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    xhttp.send(JSON.stringify({"pid":pid, "mod":mod}));
}
