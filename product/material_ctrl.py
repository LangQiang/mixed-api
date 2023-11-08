from db.db_init import *


def create_material(db: sqlite3.Connection, json):
    material_name = json['material_name']
    material_price_per = json['material_price_per']
    material_quantity_unit = json['material_quantity_unit']
    material_channel = json['material_channel']
    material_channel_contact_info = json['material_channel_contact_info']
    material_type = json.get('material_type', '')
    material_belong = json.get('material_belong', '')
    material_notes = json.get('material_notes', '')
    data = (material_name, material_price_per, material_quantity_unit, material_channel, material_channel_contact_info, material_type, material_belong, material_notes)
    print(data)
    db.execute("""INSERT OR IGNORE INTO MaterialInfo(
    material_name, 
    material_price_per, 
    material_quantity_unit,
    material_channel,
    material_channel_contact_info,
    material_type,
    material_belong,
    material_notes) VALUES (?,?,?,?,?,?,?,?)""", data)
    db.commit()


def delete_material(db: sqlite3.Connection, json):
    material_id = json['material_id']
    result = db.execute('DELETE FROM MaterialInfo WHERE material_id=?', (material_id,))
    db.commit()
    return result.rowcount > 0


def get_material_list(db: sqlite3.Connection):
    db.row_factory = dict_factory
    cursor = db.execute('SELECT * FROM MaterialInfo')
    return cursor.fetchall()
