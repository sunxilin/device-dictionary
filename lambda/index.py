
from app import query


def handler(environ, start_response):
    context = environ['fc.context']
    request_uri = environ['fc.request_uri']
    for k, v in environ.items():
        if k.startswith("HTTP_"):
            # process custom request headers
            pass

    # get request_body
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)

    # get request_method
    request_method = environ['REQUEST_METHOD']

    # get path info
    path_info = environ['PATH_INFO']

    # get server_protocol
    server_protocol = environ['SERVER_PROTOCOL']

    # get content_type
    try:
        content_type = environ['CONTENT_TYPE']
    except (KeyError):
        content_type = " "

    # get query_string
    try:
        query_string = environ['QUERY_STRING']
    except (KeyError):
        query_string = " "

    print ('request_body: {}'.format(request_body))
    print ('method: {} path: {}  query_string: {} server_protocol: {}'.format(request_method, path_info,  query_string, server_protocol))
    # do something here

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    # return value must be iterable

    result = 'Wtf???'

    if path_info == '/model':
        result = query.query_model_and_chipsets(query_string)
    
    if path_info == '/prompt/model':
        result = query.generate_query_prompt(query_string)

    print("response:" + result)

    return [result]