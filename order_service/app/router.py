from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.repository import create_order, get_order, update_order_status
from app.schemas import OrderCreateSchema, OrderSchema, OrderStatus
from app.rabbitmq import send_order_event

order_router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@order_router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def create_new_order(
    order_data: OrderCreateSchema, db: AsyncSession = Depends(get_db)
):
    new_order = await create_order(db, order_data)
    await send_order_event(
        "created", {"order_id": new_order.id, "status": new_order.status}
    )
    return new_order


@order_router.get("/{order_id}", response_model=OrderSchema)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.put("/{order_id}/status")
async def update_order(
    order_id: int, status: OrderStatus, db: AsyncSession = Depends(get_db)
):
    order = await update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await send_order_event(
        "status_updated", {"order_id": order.id, "status": order.status}
    )
    return {"status": "Order status updated"}
