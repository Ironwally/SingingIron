from bot.data.local.tinydb_interface import TinyDBInterface

# Create two separate database instances:
db1 = TinyDBInterface('db1.json', table_name='users')
db2 = TinyDBInterface('db2.json', table_name='products')

# Use TinyDBInterface methods on db1:
user_id = db1.insert({'name': 'Alice', 'email': 'alice@example.com'})
print("DB1 Users:", db1.all())

# Use TinyDBInterface methods on db2:
prod_ids = db2.insert_multiple([
    {'name': 'Widget', 'price': 9.99},
    {'name': 'Gadget', 'price': 14.99}
])
print("DB2 Products:", db2.all())

# Clean up by closing the databases:
db1.close()
db2.close()