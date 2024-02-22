var ajax = require('web.ajax');//To define ajaxvar
test_variable = document.getElementById("product_test1").value;//To get value from the required field.
ajax.jsonRpc('/my_controller', 'call', {
'result' : test_variable,
}).then(function (data_test) {});
//To receive data from python(non-mandatory)

