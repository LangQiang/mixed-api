from db.db_init import *


def create_product(db: sqlite3.Connection, json):
    product_name = json['product_name']
    product_pic = json['product_pic']
    product_type = json.get('product_type', '')
    product_classify = json.get('product_classify', '')
    product_selling_price = json['product_selling_price']
    product_notes = json.get('product_notes', '')
    data = (product_name, product_pic, product_type, product_classify, product_selling_price, product_notes)
    print(data)
    db.execute("""INSERT OR IGNORE INTO ProductInfo(
    product_name, 
    product_pic, 
    product_type, 
    product_classify, 
    product_selling_price, 
    product_notes) VALUES (?,?,?,?,?,?)""", data)
    db.commit()


def delete_product(db: sqlite3.Connection, json):
    product_id = json['product_id']
    result = db.execute('DELETE FROM ProductInfo WHERE product_id=?', (product_id,))
    db.commit()
    return result.rowcount > 0


def get_product_list(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM ProductInfo')
    return cursor.fetchall()
