from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not Found"}}

)

@router.get('/{item_id}')
def read_item(item_id: int, category: str = None):
    return {
        "제품번호": item_id,
        "제품분류": category
        }

# 형식이 없는 request body 데이터 파싱    
@router.post('/')
async def create_item(request: Request):
    """
    1. request body에 어떤 데이터가 들어있어도 됨
    2. async/await로 비동기 처리 필수
    """
    data = await request.json()
    
    return {"data": data}
