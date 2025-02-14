import inspect

#我们将创建一个自定义提示模板，该模板将函数名称作为输入，并设置提示格式以提供函数的源代码。为了实现这一点，让我们首先创建一个函数，该函数将返回给定其名称的函数的源代码。
def get_source_code(function_name):
    # Get the source code of the function
    return inspect.getsource(function_name)

def test_add():
    return 1 + 1

print(get_source_code(test_add))