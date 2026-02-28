from src.models.user import User
from src.models.order import Order, DeliveryStatus
from src.schema.order_schema import OrderRequest, OrderResponse, UpdateOrderStatusRequest
from src.utils.role import get_current_user, role_required
from src.utils.menu import menu
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends


def calculate_price(size: str, pizza_type: str, quantity: int, toppings: bool) -> float:
    """Calculate the total amount for an order based on the size, pizza type"""
    if size not in menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pizza size"
        )

    if pizza_type not in menu[size]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pizza type specified"
        )

    base_price = menu[size][pizza_type]
    toppings_price = menu[size][pizza_type].toppings if toppings else 0
    total_price = (base_price + toppings_price) * quantity
    return total_price

class OrderService:

    @staticmethod
    def create_order(db: Session, order_request: OrderRequest, current_user: User = Depends(get_current_user)) -> OrderResponse:
        """creates a new order for the current user"""
        new_order = Order(
            size=order_request.size,
            quantity=order_request.quantity,
            price=calculate_price(order_request.size, order_request.pizza_type, order_request.quantity, order_request.toppings),
            pizza_type=order_request.pizza_type,
            toppings=order_request.toppings,
            user_id=current_user.id
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    @staticmethod
    def get_order_by_id(db:Session, order_id:int, current_user= Depends(get_current_user)) -> OrderResponse:
        """retrieves an order by id by the current user"""
        order = db.query(Order).filter(Order.id== order_id, Order.user_id== current_user.id).first()
        if not order:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail= "Order not found"
            )
        return order


    @staticmethod
    def get_all_orders(db: Session, current_user= Depends(get_current_user)) -> list[OrderResponse]:
        """retrieves all orders"""
        if current_user.role == "user":
            orders = db.query(Order).filter(Order.user_id == current_user.id).all()
            return orders
        elif current_user.role == "admin":
            orders = db.query(Order).all()
            return orders


    @staticmethod
    def update_order_status( db: Session, order_id: int, new_status: UpdateOrderStatusRequest, current_user=Depends(get_current_user)) -> OrderResponse:
        """Change the status of an order given its id."""
        order_to_update = db.query(Order).filter(Order.id == order_id).first()
        if order_to_update is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
            order_to_complete.order_status = new_status.order_status
            db.commit()
            db.refresh(order_to_update)
            return order_to_update

    
    @staticmethod
    def get_order_status(db:Session, order_id:int, current_user= Depends(get_current_user)) -> OrderResponse:
        """Check the status of your order"""
        order = db.query(Order).filter_by(id = order_id, user_id = current_user.id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
                )
        # if order.user_id != current_user.id or current_user.role != "admin":
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="You are not authourized to view this order's status."
        #         )
        return order

    @staticmethod
    def delete_order(db: Session, order_id: int, current_user=Depends(get_current_user)):
        """Deletes an order"""
        order_to_delete = db.query(Order).filter_by(id = order_id, user_id = current_user.id).first()
        if order_to_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        db.delete(order_to_delete)
        db.commit()
        return {"detail": "Order deleted successfully"}