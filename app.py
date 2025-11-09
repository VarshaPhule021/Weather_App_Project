from flask import Flask, render_template, request
from constant.header import API_KEY
import requests
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        
        if request.method == 'POST':
            city = request.form['city']
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)
            data = response.json()
            

            if data['cod'] == 200:
                weather = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'].title()
                }
                
                return render_template('result.html', weather=weather)
            else:
                error = "City not found! Please enter a valid city name."
                
                return render_template('index.html', error=error)

        return render_template('index.html')    
    except Exception as e:
        error = f"An error occurred: {e}"
        
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
