import httpx
import inspect
import asyncio

def main():
    # Simulate an ASGI application
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        response_body = b'Hello, world!'
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                (b'content-type', b'text/plain'),
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': response_body,
        })

    async def make_request():
        dispatch = httpx.ASGIDispatch(app=app)
        async with httpx.AsyncClient(dispatch=dispatch) as client:
            response = await client.get('http://testserver/')
            print("Response status code:", response.status_code)
            print("Response text:", response.text)

    asyncio.run(make_request())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(httpx.ASGIDispatch))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()