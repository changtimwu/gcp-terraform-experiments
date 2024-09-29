from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import httpx

#https://cloud.google.com/docs/authentication/get-id-token#metadata-server
def idtoken_from_metadata_server_simple(url: str):
    url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity'
    headers = {'Metadata-Flavor': 'Google'}
    params = {'audience': str}
    with httpx.Client() as client:
        response = client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")

app = FastAPI()
# Serve static files (HTML page)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.get("/token")
async def get_token( target: str = None):
    if not target:
        return ''
    return idtoken_from_metadata_server_simple( target)

@app.get("/forward")
async def forward_request(target: str = None, token: str = None):
    if not target:
        raise HTTPException(status_code=400, detail="Target URL is required")
    if not token or token=="":
        token = idtoken_from_metadata_server_simple( target)
    # Forward the request to the target URL
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            print('headers=', headers)
            response = await client.get(target, headers=headers)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error forwarding request: {str(exc)}")

    # Return the response from the target URL
    return StreamingResponse(
        response.iter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

