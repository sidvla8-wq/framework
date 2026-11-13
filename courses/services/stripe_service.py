import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str, description: str = ""):
    """Создаёт продукт в Stripe."""
    product = stripe.Product.create(
        name=name,
        description=description,
    )
    return product


def create_stripe_price(product_id: str, unit_amount_cents: int, currency: str = "rub"):
    """
    Создаёт цену в Stripe.
    unit_amount_cents — цена в копейках (умножить цену курса на 100).
    """
    price = stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount_cents,
        currency=currency,
    )
    return price


def create_checkout_session(price_id: str, success_url: str, cancel_url: str):
    """
    Создаёт сессию оплаты.
    success_url — куда вернёт после успешной оплаты
    cancel_url — если пользователь закрыл окно оплаты.
    """
    session = stripe.CheckoutSession.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
