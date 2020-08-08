def app(environ, start_response):
        qs = environ['QUERY_STRING']
        res = qs.replace('&', '\n').encode('utf-8')      
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [res]
