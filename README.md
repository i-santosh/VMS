# VMS

A (VMS) Vendor Management System using Django and Django REST Framework, that will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.


# Getting Started

## Requirements

- Python 3.12.2
- pip 24.0


## Run Locally

Clone the project

```bash
  git clone https://github.com/i-santosh/VMS.git
```

Go to the project directory

```bash
  cd VMS
```

Install Requirements

```bash
  pip install -r requirements.txt
```

Make migrations

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Create superuser

```bash
  python manage.py createsuperuser --username _your-username_
```
 and it prompt for password

Start the server

```bash
  python manage.py runserver
```


## API Reference
#### Get JWT Token to access protected routes:

```python
  POST http://127.0.0.1:8000/api/auth/token/
```
it will return access and refresh Token, save it any where
| Payload | Type     |
| :-------- | :------- |
| `username` | `string` |
| `password` | `password` |

#### Refresh JWT:

```python
  POST http://127.0.0.1:8000/api/auth/token/refresh/
```
Auth in Headers must contains `Bearer _your_refresh_token_`

#### To create a new vendor :

```python
  POST http://127.0.0.1:8000/api/vendors/
```

| Payload | Type     |
| :-------- | :------- |
| `name` | `string` |
| `vendor_code` | `string` |
| `contact_details` | `string` |
| `address` | `string` |

#### Get List of vendors

```python
  GET http://127.0.0.1:8000/api/vendors/
```

#### Get Detail of specific vendor

```python
  GET http://127.0.0.1:8000/api/vendors/{vendor_id}/
```
#### Update Details of specific vendor

```python
  PUT http://127.0.0.1:8000/api/vendors/{vendor_id}/
```
| Payload | Type     |
| :-------- | :------- |
| `name` | `string` |
| `contact_details` | `string` |
| `address` | `string` |

#### Delete specific vendor

```python
  DELETE http://127.0.0.1:8000/api/vendors/{vendor_id}/
```
#### Get performance metrics specific vendor

```python
  GET http://127.0.0.1:8000/api/vendors/{vendor_id}/performance/
```

#### Create Purchase Order 

```python
  POST http://127.0.0.1:8000/api/purchase_orders/
```
| Payload | Type     |
| :-------- | :------- |
| `po_number` | `string` |
| `vendor` | `string` |
| `order_date` | `datetime` |
| `delivery_date` | `datetime` |
| `items` | `JSON` |
| `quantity` | `number` |
| `status` | `string` |
| `issue_date` | `datetime` |

- In `purchase_order` folder, there is a file name demoPOs.py that contains 10 random Purchase orders ,which can be used to create orders rapidly for test. `Consider checking vendor_code and jwt token in demoPOs.py`

#### Get List of purchase orders with filter by vendor option

```python
  GET http://127.0.0.1:8000/api/purchase_orders/?vendor_code=_example_vendor_code
```

#### Get Details of a specific Purchase Order

```python
  GET http://127.0.0.1:8000/api/purchase_orders/{po_id}/
```
#### Update a specific purchase order

```python
  PUT http://127.0.0.1:8000/api/purchase_orders/{po_id}/
```

| Payload | Type     |
| :-------- | :------- |
| `status` | `string` |
| `quality_rating` | `number` |

#### Delete a specific purchase order

```python
  DELETE http://127.0.0.1:8000/api/purchase_orders/{po_id}/
```
#### Acknowledge a specific purchase order

```python
  POST http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge/
```

| Payload | Type     |
| :-------- | :------- |
| `acknowledgment_date` | `string` |

***
- The metric updates will be done in real-time when related PO data is modified updated on every time the Purchase Order completed.

