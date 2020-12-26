

function submitRegister()
{
    var xhttp = new XMLHttpRequest();
    var form = document.getElementById("register");
    var name = form.elements.username;
    var pw = form.elements.password;
    var email = form.elements.email;
    var accesslevel = form.elements.accesslevel;
    xhttp.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200)
        {
            var response = xhttp.responseText;
            document.getElementById("response").innerHTML = response;
            form.reset();
        }
    }
    if(name <5)
    {
        alert("Username must be more than 4 chars");
        return;
    }
    if(pw < 5)
    {
        alert("Password must be more than 4 chars");
        return;
    }
    xhttp.open('POST', "/admin/registerEmployee");
    xhttp.setRequestHeader('content-type',"application/json;charset=UTF-8");
    var data = "{\"username\":\""+name.value+"\",\"password\":\""+pw.value
                +"\",\"email\":\""+email.value+"\",\"accesslevel\":\""+accesslevel.value+"\"}";
    xhttp.send(data);

    
}