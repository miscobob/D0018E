
const cachename = "basket";

function submitLogin()
{
    var form = document.forms.login;
    var basket = localStorage.getItem(cachename);
    if(basket != null)
    {
        localStorage.removeItem(cachename);
    }
    form.submit();
}

function submitRegister()
{
    var form = document.forms.register;
    var name = form.elements.name;
    var pw = form.elements.password;
    if(name < 5 && name > 13)
    {
        alert("Username must be between 5 and 12 chars");
        return;
    }
    if(pw < 5 && pw > 13)
    {
        alert("Password must be between 5 and 12 chars");
        return;
    }
    var basket = localStorage.getItem(cachename);
    if(basket != null && form.elements["basket"] != null)
    {
        var bf = document.createElement("INPUT");
        bf.name = "basket";
        bf.setAttribute("type","hidden");
        basket.removeItem("dts");
        bf.value = basket;
    }
    form.submit();
}

function cleanUp()
{
    var form = document.forms.buttonbar;
    form.setAttribute("action","/logout")
    var basket = localStorage.getItem(cachename);
    if(basket != null)
    {
        localStorage.removeItem(cachename);
    }
    form.submit();
}
