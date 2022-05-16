from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)

simple_elements = [
    {
        'data': {'id': 'lm1', 'label': 'lan_machin1 ', 'url': 'https://cdn-icons-png.flaticon.com/512/4703/4703650.png'},
        'classes': 'lan'
    },
    {
        'data': {'id': 'lm2', 'label': 'lan_machin2', 'url': 'https://cdn-icons-png.flaticon.com/512/4703/4703650.png'},
        'classes': 'lan'
    },
    {
        'data': {'id': 'sw', 'label': 'switch','url':'https://mh-2-stockagency.panthermedia.net/media/media_detail/0029000000/29763000/~ethernet-switch-icon_29763424_detail.jpg'},
        'classes':'switch'
     },

    {'data': {'source': 'sw', 'target': 'lm1'}},
    {'data': {'source': 'sw', 'target': 'lm2'}},

]

app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=simple_elements,
        layout={'name': 'breadthfirst'},
        style={'width': '500px', 'height': '500px'},
        stylesheet=[

            {
                'selector': '.lan',
                'style': {
                    'width': 70,
                    'height': 80,
                    'background-fit': 'cover',
                    'background-image': 'data(url)',
                    'content': 'data(label)'
                }
            },
            {
                'selector': '.switch',
                'style': {
                    'width': 70,
                    'height': 80,
                    'background-fit': 'cover',
                    'background-image': 'data(url)',
                    'content': 'data(label)'
                }
            },
        ]

    )
])

app.run_server(debug=True)