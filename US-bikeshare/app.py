"""
This is a flask application to show some insights on the US bikeshare dataset.

Author: Rajat Sharma
Creation Date: 20th December 2024
"""


import json
import plotly
import pandas as pd
from flask import Flask
from flask import render_template, request
from plotly.graph_objs import Bar
from src.bikeshare import load_data

app = Flask(__name__)


# data variables
CITY_DATA = {'chicago': 'data/chicago.csv',
             'new york': 'data/new_york_city.csv',
             'washington': 'data/washington.csv'}

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = [
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'all']


df_all = pd.concat([load_data("chicago", "all", "all"),
                    load_data("new york", "all", "all"),
                    load_data("washington", "all", "all")])


@app.route('/')
@app.route('/index')
def index():
    """
    Renders the main page of the bike share data explorer application.
    This function handles GET requests. On a GET request, it renders the 
    form for selecting city, month, and day.
    """

    # initializing the variables
    city = None
    month = None
    day = None

    # fetch the values from the dropdown menu
    if request.method == 'POST':
        city = request.form.get('city')
        month = request.form.get('month')
        day = request.form.get('day')


    # Grouping the data to extract the distribution of User Type
    no_of_trips = df_all.groupby("User Type").count()['Start Time']
    user_type = no_of_trips.index

    # First graph
    graphs = [
        {
            'data': [
                Bar(
                    x=user_type,
                    y=no_of_trips
                )
            ],

            'layout': {
                'title': 'Distribution of User Type',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "type"
                }
            }
        },

        ### Todo: To append second graph
        ### Checkout different graphs here: https://plotly.com/python/
        """
        'data': [
                Bar(
                    x=nlarge_names,
                    y=nlarge_counts
                )
            ],

            'layout': {
                'title': 'Title',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        },
        """
    ]






    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template(
        'master.html',
        ids=ids,
        graphJSON=graphJSON,
        cities=cities,
        months=months,
        days=days,
        city=city,
        month=month,
        day=day)


# web page that handles user query and displays results
@app.route('/go')
def go():
    """
    Handles user queries for bike share data and displays the results as a bar chart
    This function receives user selections for city, month, and day from the query parameters
    of a GET request. It then loads and filters the corresponding bike share data using the
    `load_data` function. The function then generates a bar chart visualizing the 
    distribution of user types
    """
    
    # save user input in the following variables
    city = request.args.get('city')
    month = request.args.get('month')
    day = request.args.get('day')

    # loading and filtering the data as per the selection
    df = load_data(city, month, day)

    # Grouping the data to extract the distribution of User Type
    no_of_trips = df.groupby("User Type").count()['Start Time']
    user_type = no_of_trips.index

    # Filtered graph
    graphs = [
        {
            'data': [
                Bar(
                    x=user_type,
                    y=no_of_trips
                )
            ],

            'layout': {
                'title': 'Distribution of User Type',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "type"
                }
            }
        },

        ### Todo: To append second graph
        ### Checkout different graphs here: https://plotly.com/python/
        """
        'data': [
                Bar(
                    x=nlarge_names,
                    y=nlarge_counts
                )
            ],

            'layout': {
                'title': 'Title',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        },
        """
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template(
        'go.html',
        ids=ids,
        graphJSON=graphJSON,
        cities=cities,
        months=months,
        days=days,
        city=city,
        month=month,
        day=day)


def main():
    app.run(host='0.0.0.0', port=3000, debug=True)


if __name__ == '__main__':
    main()
