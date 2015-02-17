#!/usr/bin/env python
import re

def resolve_path(path):
    urls = [(r'^$', index_page),
            (r'^([a,s,m,d])/([\d]+)/([\d]+)$'), do_math]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    # we get here if no url matches
    raise NameError

def index_page():
    """This function gives the "/" path and displays some 
    simple instructions"""
    body = [
    '<h1>A Simple Calculator</h1>', 
    '<p>In the browser, use the following notation to do simple math </p>'
    '<p>&nbsp;&nbsp;&nbsp; http://localhost:8080/operand/number1/number2  </p>'
    '<p> The operands are the following: </p>'
    '<p>&nbsp;&nbsp; a = addition </p>'
    '<p>&nbsp;&nbsp; s = subtraction </p>'
    '<p>&nbsp;&nbsp; m = multiplication</p>'
    '<p>&nbsp;&nbsp; d = division</p>'
    '<p> For example, http://localhost:8080/a/3/4 results in 7.0 </p>'
    '<p> http://localhost:8080/m/3/4 results in 12.0 </p>'
    ]
    return '\n'.join(body)

def do_math(operand, arg1, arg2):
    """This function is where the math will take place."""

    operand_list = ['a', 's', 'm', 'd']
    if operand not in operand_list:
        #status = "400 Bad Request"
        body = '<h1>Enter a correct operand letter</h1>'

    try:
        numarg1 = float(arg1)
        numarg2 = float(arg2)
    except ValueError:
        #status = "400 Bad Request"
        body = '<h1>Enter a correct number type</h1>'

    if operand == 'a': body = numarg1 + numarg2
    elif operand == 's': body = numarg1 - numarg2
    elif operand == 'm': body = numarg1 * numarg2
    elif operand == 'd':
        if numarg2 == 0: 
            #status = "400 Bad Request"
            body = '<h1>Please enter a non-zero denominator when doing division</h1>'
        else:
            body= numarg1 / numarg2
    return '\n'.join(body)

def web_calculator_application(environ, start_response):
    "A WSGI application making a web calculator within the URL"
    headers = [("Content-type", "text/html")]

    try:    
        path = environ.get('PATH_INFO', None)
        if path is None:
                raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, web_calculator_application)
    srv.serve_forever()