import asyncio

from fastapi import APIRouter
from starlette.responses import JSONResponse

from middleware import Reader, WayDirector, List
from model import Path

router = APIRouter()
reader = Reader("sheet.csv")

@router.get("/citiesfrom")
async def citiesfrom():
    return JSONResponse(content = await reader.get_from(), status_code=200)

@router.get("/citiesto")
async def citiesto():
    return JSONResponse(content = await reader.get_to(), status_code=200)

@router.get("/path/{origin}/{destination}", response_model=List[Path])
async def path(origin: str, destination: str):
    try:
        director = WayDirector("sheet.csv", origin, destination)
        ways = await asyncio.gather(
            director.calculate_routes("cost", "cost"),
            director.calculate_routes("days", "days"),
            director.calculate_routes(lambda u, v, d: 0.3 * d['days'] + 0.7 * d['cost'], "opt"),
        )
        return JSONResponse(content=ways, status_code=200)
    except ValueError as e:
        return JSONResponse(content=str(e), status_code=400)