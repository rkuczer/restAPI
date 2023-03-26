from urllib import request

from flask import Flask, jsonify
import requests

app = Flask(__name__)

drinks = [    {'name': 'Soda', 'price': 2.50},    {'name': 'Tea', 'price': 3.00},    {'name': 'Coffee', 'price': 4.00}]

cocktails = [    {'name': 'Margarita', 'ingredients': ['Tequila', 'Lime Juice', 'Cointreau'], 'price': 8.50},
    {'name': 'Old Fashioned', 'ingredients': ['Bourbon', 'Angostura Bitters', 'Sugar', 'Orange Peel'], 'price': 10.00},
    {'name': 'Mojito', 'ingredients': ['Rum', 'Mint', 'Lime Juice', 'Sugar', 'Club Soda'], 'price': 9.00}
]

@app.route('/drinks')
def get_drinks():
    return jsonify({'drinks': drinks})

@app.route('/cocktails')
def get_cocktails():
    return jsonify({'cocktails': cocktails})

@app.route('/drinks/<string:name>')
def get_drink_by_name(name):
    for drink in drinks:
        if drink['name'] == name:
            return jsonify(drink)
    return jsonify({'message': 'Drink not found'})

@app.route('/cocktails/<string:name>')
def get_cocktail_by_name(name):
    for cocktail in cocktails:
        if cocktail['name'] == name:
            return jsonify(cocktail)
    return jsonify({'message': 'Cocktail not found'})

@app.route('/drinks', methods=['POST'])
def add_drink():
    new_drink = {'name': request.json['name'], 'price': request.json['price']}
    drinks.append(new_drink)
    return jsonify(new_drink)

@app.route('/cocktails', methods=['POST'])
def add_cocktail():
    new_cocktail = {'name': request.json['name'], 'ingredients': request.json['ingredients'], 'price': request.json['price']}
    cocktails.append(new_cocktail)
    return jsonify(new_cocktail)


@app.route('/hello')
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    app.run()