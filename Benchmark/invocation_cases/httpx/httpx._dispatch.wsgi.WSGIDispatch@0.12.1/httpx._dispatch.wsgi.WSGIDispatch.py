import httpx
import inspect

def main():
    # Simulate a WSGI application
    def simple_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"Hello, World"]

    # Create a WSGIDispatch instance
    dispatch = httpx.WSGIDispatch(app=simple_app)
    
    # Make a request using the WSGIDispatch
    with httpx.Client(dispatch=dispatch) as client:
        response = client.get("http://testserver/")
        print("WSGIDispatch response:", response.text)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx.WSGIDispatch))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()