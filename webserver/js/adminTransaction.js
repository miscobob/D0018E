
function getTranscations()
{
    var field = document.getElementById("data");
    var data = field.value;
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
                if(transactions.hasOwnProperty("message"))
                {
                    alert(transactions["message"]);
                    return;
                }
                if( Object.keys(transactions).length == 0)
                {
                    document.getElementById("response").innerHTML = "No transactions found";
                }
                else{
                    document.getElementById("response").innerHTML = "";
                    for(var i in transactions)
                    {
                        var row = document.createElement("DIV");
                        row.setAttribute("class","trow");
                        row.innerHTML = "Transaction:"+i+"<br>";
                        parseTransaction(transactions[i], row);
                        document.getElementById("response").appendChild(row);
                    }
                }
            }
            else
            {
                alert("No transactions found");
            }
        }
    }
    xhttp.open("POST","#", true);
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    xhttp.send("{\"var\":\""+data+"\"}");
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