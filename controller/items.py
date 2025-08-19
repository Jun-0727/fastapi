import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not Found"}}

)

class Item(BaseModel):
    id: int
    name: str
    price: int
    category: str

# Load .env file
load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, echo=True)

# 아이템 목록 조회
@router.get('/')
def read_items():
    
    select_item_query_text = text(f"SELECT * FROM item")
    
    with engine.connect() as conn:
        response_cursor = conn.execute(select_item_query_text)

        rows = response_cursor
        result = [dict(row._mapping) for row in rows]

    return {"result": result}

# 아이템 조회
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
# @router.post('/')
# async def create_item(request: Request):
#    """
#    1. request body에 어떤 데이터가 들어있어도 됨
#    2. async/await로 비동기 처리 필수
#    """
#    data = await request.json()
#    
#    return {"data": data}

# 아이템 생성
@router.post('/')
def create_item(item: Item):
    """
    1. request body에 Model(Item)의 모든 필드가 들어있어야 함
    """
    create_item_query_text = text(f"INSERT INTO item VALUES({item.id}, '{item.name}', {item.price}, '{item.category}')")
    with engine.connect() as conn:
        conn.execute(create_item_query_text)
        conn.commit()
    
    return {"success": True}

# 아이템 이름 수정
@router.put('/{item_id}')
def update_item(item_id: int, item: Item):
    
    update_item_query_text = text(f"UPDATE item SET name = '{item.name}' WHERE item_id = {item_id}")
    with engine.connect() as conn:
        conn.execute(update_item_query_text)
        conn.commit()

    return {"success": True}

# 아이템 삭제
@router.delete('/{item_id}')
def delete_item(item_id: int):
    delete_item_query_text = text(f"DELETE FROM item WHERE item_id = {item_id}")
    with engine.connect() as conn:
        conn.execute(delete_item_query_text)
        conn.commit()

    return {"success": True}
