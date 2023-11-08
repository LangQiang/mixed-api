from db.db_init import *


def create_cost_component(db: sqlite3.Connection, json):
    product_id = json['product_id']
    product_components = json['product_components']
    components = []
    for ele in product_components:
        product_component_id = int(ele['product_component_id'])
        product_component_name = ele['product_component_name']
        product_component_amount = float(ele['product_component_amount'])
        components.append((product_id, product_component_id, product_component_name, product_component_amount))
    print(components)

    db.executemany('INSERT OR REPLACE INTO ProductComponent(product_id, product_component_id, product_component_name,product_component_amount) VALUES (?,?,?,?)', components)
    db.commit()


def get_cost_component_list(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM ProductComponent')
    return cursor.fetchall()
