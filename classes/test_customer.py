from classes.customer import Customer

customer_data = {
    "email": "john@doe.com",
    "password": "password",
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Main St",
    "phone": "123-456-7890"
}


def test_customer_init():
    email_mix_case = 'jOhN@dOe.cOm'
    email_lower_case = email_mix_case.lower()
    customer = Customer(email_mix_case)
    assert customer.email == email_lower_case


def test_customer_is_new_customer():
    customer = Customer(customer_data['email'])
    assert customer.is_new_customer() is True


def test_register_customer():
    email = 'jOhN@dOe.cOm'
    customer = Customer(email)
    customer.register_customer(
        'John', 'Doe', '123 Main St', '123-456-7890', 'password')
    assert customer.is_new_customer() is False
