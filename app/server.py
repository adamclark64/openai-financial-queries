from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

# pkgs
from openai_financial_helper import chain as openai_financial_helper_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# ////////////////////////////////////////////////////////////

add_routes(app, openai_financial_helper_chain, path="/openai-financial-helper-chain")

# ////////////////////////////////////////////////////////////

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
