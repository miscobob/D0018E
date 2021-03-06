
async function loadBasket()
{
    const TTL = 3600000
    var cache = localStorage.getItem(cachename);
    if(cache == null)
    {
        loadFromServer();
    }
    else
    {
        var basket;
        try {
            basket = JSON.parse(cache);
        } catch (error) {
            console.warn(error);
            basket = JSON.parse(JSON.stringify(cache));
        }
        var dts = Date.parse(basket.dts);
        console.log(dts-Date.now()>-TTL)
        if(!(dts-Date.now()>-TTL))
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


function loadFromServer(bool = true)
{
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange =  function()
    {
        if(this.readyState == 4 && this.status == 200)
        {
            var response = this.responseText;
            var basket = JSON.parse(response);
            console.log(basket)
            if(basket.products.length)
            {
                var date = new Date();
                basket.dts = date.toISOString();
                localStorage.setItem(cachename, JSON.stringify(basket));
                generateHTML(basket);
            }
            else if(localStorage.getItem(cachename))
            {
                localStorage.removeItem(cachename)
            }

            
        } 
    }
    xhttp.open("GET", "/loadBasket", bool);
    xhttp.send();
}

function generateHTML(basket)
{
    console.log(basket);
    var products = basket.products;
    var table = document.getElementById("basketArea");
    table.innerHTML="";
    var i;
    console.log(products);
    for(i in products)
    {
        var row = document.createElement("DIV");
        row.className = "basketRow";
        row.id = "row" + products[i].pid;
        
        var image = document.createElement("AMP-IMG");
        image.setAttribute("height","9");
		image.setAttribute("width","16");
		image.setAttribute("src",products[i].path);
        image.setAttribute("layout","responsive");
        image.setAttribute("class","fixedsizedItem");
        ///image.style.display = "table-cell";
        row.appendChild(image)
        
        var text = document.createElement("P");
        text.innerHTML = '<a href ="/products/'+products[i].pid+'">' + products[i].name + "</a> by "+ products[i].make + " priced at " +products[i].price;
        ///text.style.display = "table-cell";
        text.setAttribute("class","basketItem");
        var form = document.createElement("FORM");
        var field = document.createElement("INPUT");
        field.setAttribute("type", "text");
        field.value = products[i].count;
        field.id = "count"+products[i].pid;
        ///field.setAttribute("onkeyup","this.value=this.value.replace(/[^\d]/,'')" )
        ///field.setAttribute("onChange","changeCount("+products[i].pid+", this.value)");
        field.readOnly = true;
        form.appendChild(field);
        text.appendChild(form);
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

async function changeCount(pid, value)
{
    if(typeof(value) != Number)
    {
        try {
            value = parseInt(value)
        } catch (error) {
            alert("tried to change value to non integer")
            var e = document.getElementById("count"+pid);
            if(e != null)
            {
                e.value = value;
            }
        }
    }
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
                var mod = value - products[i].count;
                products[i].count = value;
                if (products[i].count == 0)
                {
                    if (i == 0)
                        products.splice(0,1);
                    else
                        products.splice(i,i);
                }
                updateServer(pid, mod);
                localStorage.setItem(cachename, JSON.stringify(basket));
                return;
            }
        }
    }
    alert("No entry in storage to change");
}

async function increaseCount(pid)
{
    const mod = 1
    var cache = localStorage.getItem(cachename);
    if(cache != null)
    {
        try {
            var basket = JSON.parse(cache);
        } catch (error) {
            console.warn(error);
            var basket = JSON.parse(JSON.stringify(cache));
        }
        var products = basket.products;
        var i;
        for( i in products)
        {
            if(products[i].pid == pid)
            {
                products[i].count += mod;
                localStorage.setItem(cachename, JSON.stringify(basket));
                var e = document.getElementById("count"+pid);
                if(e != null)
                {
                    e.value = products[i].count;
                }
                updateServer(pid, mod);
                return;
            }
        }
        requestJSON(pid, mod);
        return;
    }
    requestJSON(pid, mod, false);
}

async function decreaseCount(pid)
{
    const mod = 1
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
                products[i].count -= mod;
                if (products[i].count == 0)
                {
                    if (i == 0)
                        products.splice(0,1);
                    else
                        products.splice(i,i);
                    var e = document.getElementById("row"+pid);
                    if(e != null)
                    {
                        e.innerHTML = "";
                        e.remove();
                    }
                }
                updateServer(pid, -mod);
                localStorage.setItem(cachename, JSON.stringify(basket));
                var e = document.getElementById("count"+pid);
                if(e != null)
                {
                    e.value = products[i].count;
                }
                return;
            }
        }
    }
    alert("Product not in basket");
}



function requestJSON(pid, mod, hasBasket = true)
{
    var xhttp = new XMLHttpRequest();
    //console.log(basket)
    xhttp.onreadystatechange =  function()
    {
        if(this.readyState == 4 && this.status == 200)
        {
            var response = this.responseText;
            if(response == "" || response == null)
            {
                alert("You tried to add a non existing product!");
                return;
            }
            else
            {
                try{
                    var jsobj = JSON.parse(response.toString());
                    if(jsobj.hasOwnProperty("message"))
                    {
                        alert(jsobj.message);
                        return;
                    }
                    if(hasBasket)
                    {
                        var cache = localStorage.getItem(cachename);
                        var basket = JSON.parse(cache);
                        basket.products.push(jsobj);
                        localStorage.setItem(cachename, JSON.stringify(basket));
                    }
                    else if(!isEmpty(jsobj)){
                        var date = new Date();
                        jsobj.dts = date.toISOString();
                        localStorage.setItem(cachename, JSON.stringify(jsobj));
                    }
                    else
                    {
                        alert("Product not found")
                        return;
                    }
                }
                catch
                {
                    alert("ERROR OCCOURED")
                    return;
                }
            }
        }
    }
    xhttp.open("POST", "/addProductToBasket", true);
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    var data = {"pid":pid, "mod":mod, "hasBasket":hasBasket}
    xhttp.send(JSON.stringify(data));
}

function isEmpty(obj)
{
    for(i in obj)
    {
        return false;
    }
    return true;
}

function updateServer(pid, mod)
{
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/updateBasket", true);
    xhttp.onreadystatechange = function()
    {
        var text = this.responseText;
        if(text != "")
        {
            localStorage.removeItem(cachename);
            alert(text + "\n basket will be cleared");
        }
    }
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    var data = {"pid":pid, "mod":mod}
    xhttp.send(JSON.stringify(data));
}

function checkout()
{
    loadFromServer(bool = false);
    var cache = localStorage.getItem(cachename)
    console.log(cache)
    if(!cache)
    {
        alert("basket is empty");
        return;
    }
    var basket = JSON.parse(cache);
    var products = basket.products;
    var confirm = "Confirm purchase of:";
    var totalprice = 0;
    for(i in products)
    {
        totalprice += products[i].price * products[i].count;
        confirm+="\n"+products[i].name + " by " + products[i].make + ", " + products[i].count + " x " +products[i].price + " = " + (products[i].price * products[i].count);
    }
    confirm+= "\n total price of:"+totalprice;
    if(window.confirm(confirm))
    {
        var button = document.getElementById("checkout");
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function()
        {
            var response = this.responseText;
            var answer = JSON.parse(response);
            console.log(response)
            if(answer.success)
            {
                localStorage.removeItem(cachename);
                var table = document.getElementById("basketArea");
                table.innerHTML = "";
            }
            alert(answer.message);
            location.reload();
        };
        
        xhttp.open("GET", "/checkout", true);
        xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
        xhttp.send(); 
    }
}
