from fastapi import APIRouter

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
