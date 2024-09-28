from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

# Serve static files (HTML page)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.get("/forward")
async def forward_request(target: str = None):
    if not target:
        raise HTTPException(status_code=400, detail="Target URL is required")

    # Forward the request to the target URL
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target)
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

