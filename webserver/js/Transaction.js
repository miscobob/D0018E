var loaded = false;

function getTranscations()
{
    if(loaded)
    {
        return;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200)
        {
            /*
            {trans:[{prd1},{prd2}]}
            */
            var response = xhttp.responseText;
            if(response != ""){
                var transactions = JSON.parse(response);
                for(var i in transactions)
                {
                    var row = document.createElement("DIV");
                    row.setAttribute("class","trow")
                    row.innerHTML = "Transaction:"+i+"<br>";
                    parseTransaction(transactions[i], row)
                    document.getElementById("response").appendChild(row)
                }
                loaded = true;
            }
            else
            {
                alert("No transactions found")
            }
        }
    }
    xhttp.open("GET","/loadTransactions", true);
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    xhttp.send();
}


function parseTransaction(transaction, element)
{
    for(i in transaction)
    {
        var trans = document.createElement("DIV");
        trans.setAttribute("class", "trow");
        trans.innerHTML= "product: <i>" + transaction[i].name +"</i> by <i>"+ transaction[i].make+ "</i> |price: " + transaction[i].price + "$ |count:" +transaction[i].count;
        element.appendChild(trans);
    }
}