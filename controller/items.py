from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not Found"}}

)

class Item(BaseModel):
    category: str
    item_id: int
    item_name: str
    item_price: int


@router.get('/{item_id}')
def read_item(item_id: int, category: str = None):
    return {
        "제품번호": item_id,
        "제품분류": category
        }


"""
    같은 경로의 함수가 정의돼있는 경우 가장 위쪽에 있는 메서드가 적용된다
"""

# 형식이 없는 request body 데이터 파싱    
@router.post('/')
async def create_item(request: Request):
    """
    1. request body에 어떤 데이터가 들어있어도 됨
    2. async/await로 비동기 처리 필수
    """
    data = await request.json()
    
    return {"data": data}


# 형식이 있는 request body 데이터(itme) 파싱
@router.post('/')
def create_item(item: Item):
    """
    1. request body에 Model(Item)의 모든 필드가 들어있어야 함
    """

    return {"item": item}
