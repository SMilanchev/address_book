from fastapi import FastAPI
import uvicorn

from address_book.views import address_router
import settings

app = FastAPI()
app.include_router(address_router)

if __name__ == '__main__':
    uvicorn.run("api:app", host=settings.AB_HOST, port=settings.AB_PORT, reload=True)
