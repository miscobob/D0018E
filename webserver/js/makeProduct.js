function makeProduct(dict)
{
    var dictstring = JSON.stringify(dict);

    var fs = require('fs');
    fs.writeFile("products.json", dictstring, function(err, result) {
        if(err) console.log('error', err);
    });
}
