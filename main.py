import pickle
from flask import Flask, render_template, request

# create an object of class Flask
app = Flask(__name__)
model = pickle.load(open('lin_reg_model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    try:
        year = int(request.form.get('Year'))
        present_price = float(request.form.get('Present_Price'))
        kms_driven = int(request.form.get('Kms_Driven'))
        
        # Convert categorical values to numeric
        fuel_type = request.form.get('Fuel_Type')
        fuel_type_dict = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
        if fuel_type in fuel_type_dict:
            fuel_type = fuel_type_dict[fuel_type]
        else:
            raise ValueError("Invalid Fuel Type")
        
        seller_type = request.form.get('Seller_Type')
        seller_type_dict = {'Dealer': 0, 'Individual': 1}
        if seller_type in seller_type_dict:
            seller_type = seller_type_dict[seller_type]
        else:
            raise ValueError("Invalid Seller Type")
        
        transmission = request.form.get('Transmission')
        transmission_dict = {'Manual': 0, 'Automatic': 1}
        if transmission in transmission_dict:
            transmission = transmission_dict[transmission]
        else:
            raise ValueError("Invalid Transmission Type")
        
        owner = int(request.form.get('Owner'))

        features = [[year, present_price , kms_driven, fuel_type, seller_type, transmission, owner]]

        prediction = model.predict(features)
        output = round(prediction[0], 2)
        # print(output)
        return render_template('index.html', prediction_text = f'The predicted price of Car is {output} lakhs')
    
    except ValueError as e:
        return render_template('index.html', prediction_text='Please fill the form correctly.')


if __name__=='__main__':
    app.run(debug=True)
 