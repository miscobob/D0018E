
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
    xhttp.open('POST', "/admin/addProduct");
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    var data = "{\"name\":\""+name.value+"\",\"make\":\""+make.value
                +"\",\"price\":\""+price.value+"\",\"stock\":\""+stock.value+"\"}";
    xhttp.send(data);

    
}