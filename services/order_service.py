from database import get_db_connection

class OrderService:

    @staticmethod
    def create_order(order_data: dict):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """INSERT INTO orders 
        (customer_name, phone, address, product, flavor, message, price, payment_type, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (
            order_data.get('customer_name'),
            order_data.get('phone'),
            order_data.get('address'),
            order_data.get('product'),
            order_data.get('flavor'),
            order_data.get('message'),
            order_data.get('price'),
            order_data.get('payment_type'),
            "pending"   # ✅ status fix
        )

        cursor.execute(query, values)
        conn.commit()

        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return new_id


    @staticmethod
    def fetch_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM orders")
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results