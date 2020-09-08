# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# flask_restful do jsonify automatically
class Item(Resource): # Inheritance: Student inherit Resource
    parser = reqparse.RequestParser()
    # parser is used to extract only the information that we want
    parser.add_argument('price',
        type=float,
        required=True, # required field, if price is not in the request body -> error message
        help="This field cannot be left blank!" # error message
    )
    parser.add_argument('store_id',
        type=int,
        required=True, # required field, if price is not in the request body -> error message
        help="Every item needs a store id." # error message
    )

    @jwt_required()
    def get(self, name):
        # it could be called by self. or Item.
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message' : 'Item not found'}, 404

    def post(self, name):
        # it could be called by self. or Item.
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exists.".format(name)}, 400 # bad request

        data = Item.parser.parse_args() # json format

        item = ItemModel(name, **data) # ** = data['price'], data['store_id']

        try:
            # item.insert()
            item.save_to_db()
        except:
            return {"message" : "An error occurred inserting the item."}, 500 # internal server error

        return item.json(), 201 # 201 is for creating
    
    def delete(self, name):
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message' : 'Item deleted'}
        '''

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message' : 'Item deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args() # json format
        
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])

        if item is None:
            '''
            try:
                updated_item.insert()
            except:
                return {"message" : "An error occurred inserting the item."}, 500
            '''
            item = ItemModel(name, **data) # data['price'], data['store_id']
        else:
            '''
            try:
                updated_item.update()
            except:
                return {"message" : "An error occurred updating the item"}, 500
            '''
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()

        # return updated_item.json()
        return item.json()
    

class ItemList(Resource):
    def get(self):
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name' : row[0], 'price' : row[1]})

        connection.close()

        return {'items' : items}
        '''

        # List comprehension
        return {'items' : [item.json() for item in ItemModel.query.all()]} # ItemModel.query.all() returns all of the objects in the database
        # return {'items' : list(map(lambda x: x.json(), ItemModel.query.all()))}
