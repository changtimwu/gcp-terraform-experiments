from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import httpx

import google
import google.oauth2.credentials
from google.auth import compute_engine
import google.auth.transport.requests
import urllib
import google.oauth2.id_token



def make_request_with_credential(url: str):
    """
    Use the Google Cloud metadata server in the Cloud Run (or AppEngine or Kubernetes etc.,)
    environment to create an identity token and add it to the HTTP request as part of an
    Authorization header.

    Args:
        url: The url or target audience to obtain the ID token for.
            Examples: http://www.example.com
    """
    request = google.auth.transport.requests.Request()
    # Set the target audience.
    # Setting "use_metadata_identity_endpoint" to "True" will make the request use the default application
    # credentials. Optionally, you can also specify a specific service account to use by mentioning
    # the service_account_email.
    credentials = compute_engine.IDTokenCredentials(
        request=request, target_audience=url, use_metadata_identity_endpoint=True
    )

    # Get the ID token.
    # Once you've obtained the ID token, use it to make an authenticated call
    # to the target audience.
    print("request before:", request)
    credentials.refresh(request)
    # print(credentials.token)
    print("request after ID token update:", request)
    return request


def make_authorized_get_request(endpoint, audience):
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified audience value.
    """
    # Cloud Functions uses your function's URL as the `audience` value
    # audience = https://project-region-projectid.cloudfunctions.net/myFunction
    # For Cloud Functions, `endpoint` and `audience` should be equal
    req = urllib.request.Request(endpoint)
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)
    return response.read()

#https://cloud.google.com/docs/authentication/get-id-token#metadata-server
def idtoken_from_metadata_server_simple(url: str):
    url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity'
    headers = {'Metadata-Flavor': 'Google'}
    params = {'audience': url}
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
    return idtoken_from_metadata_server( target)

@app.get("/forward")
async def forward_request(target: str = None):
    if not target:
        raise HTTPException(status_code=400, detail="Target URL is required")
    async with httpx.AsyncClient() as client:
        try:
            response = make_request_with_credential( target)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error forwarding request: {str(exc)}")
    # Return the response from the target URL
    return StreamingResponse(
        response.iter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers)
    )

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
    import os
    portno = os.environ.get('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=int(portno))

