from typing import Literal, Union, Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
import logfire

app = FastAPI()

logfire.configure()
logfire.instrument_pydantic()
# logfire.instrument_fastapi(app)


class Item(BaseModel):
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None
    q: str | None = None

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/query/")
async def read_query_params(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/path/{item_id}")
def item_path(item_id: int = Path(..., title="The ID of the item to get"), q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id, **item.dict()}

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(alias="item-query",
                                                    title="Query string",
                                                    description="Query string for the items to search in the database that have a good match",
                                                    min_length=3,
                                                    max_length=50,
                                                    pattern="^fixedquery$",
                                                    deprecated=True,)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items/{item_id}")
async def test(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
