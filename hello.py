def function_1():
    var_1 = "one"
    var_2 = "two"
    var_3 = "three"
    return var_1,var_2,var_3

def function_2():
    print(var_1,var_2,var_3)


var_1, var_2, var_3 = function_1()
function_2()