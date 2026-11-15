import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name, description):
    """Создает продукт в Stripe."""
    return stripe.Product.create(
        name=name,
        description=description,
    )


def create_stripe_price(product_id, unit_amount_cents, currency="rub"):
    """Создает цену: сумма в копейках, привязана к product_id."""
    return stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount_cents,   # именно целое число копеек
        product=product_id,              # id ПРОДУКТА, созданного шагом раньше
    )


def create_checkout_session(price_id, success_url, cancel_url):
    """Создает сессию оплаты. Обратите внимание: передается именно price_id."""
    session = stripe.checkout.Session.create(
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def retrieve_checkout_session(session_id):
    """Получает сессию по id — для проверки статуса платежа."""
    return stripe.checkout.Session.retrieve(session_id)
