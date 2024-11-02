from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models import Order, OrderItem
from app.schemas import OrderCreateSchema, OrderStatus


async def create_order(db: AsyncSession, order_data: OrderCreateSchema):
    new_order = Order(user_id=order_data.user_id, status=OrderStatus.pending)
    db.add(new_order)
    await db.flush()  # Obtenha o ID do pedido antes de criar itens

    order_items = [
        OrderItem(
            order_id=new_order.id, product_id=item.product_id, quantity=item.quantity
        )
        for item in order_data.items
    ]
    db.add_all(order_items)
    await db.commit()
    await db.refresh(new_order)
    return new_order


async def get_order(db: AsyncSession, order_id: int):
    query = select(Order).options(joinedload(Order.items)).where(Order.id == order_id)
    result = await db.execute(query)
    return result.scalars().first()


async def update_order_status(db: AsyncSession, order_id: int, new_status: OrderStatus):
    order = await get_order(db, order_id)
    if order:
        order.status = new_status
        await db.commit()
        await db.refresh(order)
    return order
