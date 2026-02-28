from src.service.order_service import OrderService
from src.schema.order_schema import OrderRequest, OrderResponse, UpdateOrderStatusRequest
from src.utils.role import role_required, get_current_user
from src.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

order_router = APIRouter()

@order_router.post(
    path="/order",
    response_model=OrderResponse,
    status_code=201,
    summary="create a new order",
    description="This endpoint create a new order",
    responses={
        201: {
            "description": "Order created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "size": "medium",
                        "quantity": 2,
                        "price": 25.6,
                        "pizza_type": "margarita",
                        "toppings": "mushrooms, olives",
                        "order_status": "pending",
                        "user_id": 345,
                        "address": "123 Pizza St, Flavor Town"
                    }
                }
            }
        },
        400:{
            "description": "Bad Request - Invalid order details",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid pizza size"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - Invalid or missing token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authorization token is missing"
                    }
                }
            }
        }
    }   
)
def create_order(
    order_request : OrderRequest,
    db: Session= Depends(get_db),
    current_user = Depends(role_required(["user"]))
    ) -> OrderResponse:
    """It endpoint creates a new order for the user"""
    order = OrderService.create_order(db, order_request, current_user)
    return order

@order_router.get(
    path= "/order/{order_id}",
    response_model = OrderResponse,
    status_code=200,
    summary= "Get order by ID",
    description = "This endpoint retrieves an order by its id for the current user",
    responses = {
        200: {
            "description": "Order retrived successfully",
            "content":{
                "application/json":{
                    "example":{
                        "id" : 1,
                        "size": "medium",
                        "quantity": 4,
                        "price": 65,
                        "pizza-type": "pepperoni",
                        "toppings": "extra cheese",
                        "order_status" : " in-transit"
                    }
                }
            }
        },
         401: {
            "description": "Unauthorized - Invalid or missing token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authorization token is missing"
                    }
                }
            }
        },
        404: {
            "description": "Not Found - Order does notexist",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Order not found"
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authorization token is missing"
                    }
                }
            }
        }
    }
)
def get_order_by_id(
    order_id:int,
    db: Session=Depends(get_db),
    current_user= Depends(role_required(["user"]))
) -> OrderResponse:
    """This endpoint retrieves an order by its id for the current user"""
    order = OrderService.get_order_by_id(db, order_id, current_user)
    return order
    

@order_router.get(
    "/orders",
    response_model= list[OrderResponse],
    status_code=200,
    summary="Get all orders",
    description="This endpoint retrieves all orders. Admins can see all orders, users can see their own orders only.",
    responses={
        200: {
            "description": "Order retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "size": "medium",
                            "quantity": 4,
                            "price": 65,
                            "pizza_type": "pepperoni",
                            "toppings": "extra cheese",
                            "order_status": "in-transit"
                        },
                        {
                            "id": 3,
                            "size": "medium",
                            "quantity": 4,
                            "price": 65,
                                                        "price": 65,
                            "pizza_type": "pepperoni",
                            "toppings": "extra cheese",
                            "order_status": "in-transit"
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Unauthorized - Invalid or missing token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authorization token is missing"
                    }
                }
            }
        },
        404: {
        "description": "Not Found - No orders available",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No orders found"
                }
            }
        }
    }
}
)
def get_all_orders(db: Session = Depends(get_db), current_user = Depends(role_required(["admin", "user"]))) -> list[OrderResponse]:
    """This endpoint retrieves all orders. Admins can see all orders, users can see their own orders only."""
    orders = OrderService.get_all_orders(db, current_user)
    return orders

@order_router.patch(
    "/orders/{order_id}/status",
    response_model=OrderResponse,
    status_code=200,
    summary="Update order status",
    description="This endpoint updates the status of an order by its id. Only authorized users can update order status.",
    responses={
        200: {
            "description": "Order status updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "size": "medium",
                        "quantity": 4,
                        "price": 65,
                        "pizza_type": "pepperoni",
                        "toppings": "extra cheese",
                        "order_status": "delivered"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - Invalid or missing token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authorization token is missing"
                    }
                }
            }
        },
        404: {
            "description": "Not Found - Order does not exist",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Order not found"
                    }
                }
            }
        }
    }
)
def update_order_status(
    order_id: int,
    new_status: UpdateOrderStatusRequest,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["admin"]))
) -> OrderResponse:
    """This endpoint updates the status of an order by its id"""
    order = OrderService.update_order_status(db, order_id, new_status, current_user)
    return order

@order_router.get(
    "/orders/{order_id}/status",
    response_model=OrderResponse,
    status_code=200,
    summary="Get order status",
    description="This endpoint retrieves the status of an order by its id for the current user.",
    responses={
        200: {
            "description": "Order status retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "order_status": "pending"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - Invalid or missing token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authorization token is missing"
                    }
                }
            }
        },
        403: {
            "description": "Forbidden - Not authorized to view this order",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You are not authourized to view this order's status."
                    }
                }
            }
        },
        404: {
            "description": "Not Found - Order does not exist",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Order not found"
                    }
                }
            }
        }
    }
)
def get_order_status(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["user", "admin"]))
):
    """This endpoint retrieves the status of an order by its id"""
    status = OrderService.get_order_status(db, order_id, current_user)
    return status

@order_router.delete(
    path="/order/{order_id}",
    status_code=200,
    summary="delete an order",
    description="This endpoint deletes an order belonging to the authenticated user",
    responses={
        200: {
            "description": "Order deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Order deleted successfully"
                    }
                }
            }
        },
        404: {
            "description": "Order not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Order not found"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - Invalid or missing token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Authorization token is missing"
                    }
                }
            }
        }
    }
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(role_required(["user"]))
):
    """This endpoint deletes an order for the authenticated user"""
    return OrderService.delete_order(
        db=db,
        order_id=order_id,
        current_user=current_user
    )
