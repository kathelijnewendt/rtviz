#!/usr/bin/env python

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(description='An interactive dashboard for easy inspection of reading times data.')
    parser.add_argument('input_file', help='Path to the .csv file containing reading times data.')
    parser.add_argument('-a', '--align', action='store_true', required=False,
                        help='Align the chart based on the index of a word of interest.')
    args = parser.parse_args()

    df = pd.read_csv(args.input_file)

    if args.align:
        df = assign_adjusted_word_indices(df)
        x_axis_label = 'Adjusted Word Index'
    else:
        df['Adjusted Word Index'] = df['Word Index']
        x_axis_label = 'Word Index'

    app = Dash()

    colors = {
        'background': '#F5FBFF',  # Ghost White
        'text': '#00008B'  # Dark Blue
    }

    app.layout = html.Div(children=[
        html.H1(
            children='Reading Times Dashboard',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'font-family': 'Courier New'
            }
        ),

        html.Label(children='Select condition(s):',
                   style={'font-family': 'Courier New'}),
        dcc.Dropdown(
            id='condition-filter',
            options=[{'label': 'All', 'value': 'All'}] + [{'label': str(c), 'value': c} for c in df['Condition'].unique()],
            value=['All'],
            multi=True,
            placeholder='Select one or more conditions'
        ),

        html.Label(children='Select global index range:',
                   style={'font-family': 'Courier New'}),
        dcc.RangeSlider(
            id='global-index-slider',
            min=df['Global Index'].min(),
            max=df['Global Index'].max(),
            step=1,
            marks={i: str(i) for i in range(df['Global Index'].min(), df['Global Index'].max() + 1)},
            value=[df['Global Index'].min(), df['Global Index'].max()]
        ),

        html.Button(children='Reset filter', id='reset-filter', n_clicks=0,
                    style={'font-family': 'Courier New'}),

        dcc.Graph(id='rt-chart')
    ])

    @app.callback(
        Output('rt-chart', 'figure'),
        [Input('condition-filter', 'value'),
         Input('global-index-slider', 'value')]
    )
    def update_chart(selected_conditions, global_index_range):
        if 'All' in selected_conditions:
            selected_conditions = df['Condition'].unique()

        filtered_df = df[df['Condition'].isin(selected_conditions)]

        filtered_df = filtered_df[
            (filtered_df['Global Index'] >= global_index_range[0]) &
            (filtered_df['Global Index'] <= global_index_range[1])
            ]

        fig = px.line(
            filtered_df,
            x='Adjusted Word Index',
            y='RT(s)',
            color='Condition',
            line_group='Global Index',
            markers=True,
            hover_name='Word',
            hover_data={
                'Condition': False,
                'Global Index': True,
                'Sentence Index': True,
                'Word Index': True
            }
        )
        fig.update_traces(mode='lines+markers')

        fig.update_layout(
            font_family='Courier New',
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            xaxis_title=x_axis_label
        )

        fig.update_xaxes(
            mirror=True,
            tick0=1,
            dtick=1,
            showline=True,
            linecolor='black',
            gridcolor='white'
        )

        fig.update_yaxes(
            mirror=True,
            showline=True,
            linecolor='black',
            gridcolor='white'
        )

        return fig

    @app.callback(
        Output('condition-filter', 'value'),
        Output('global-index-slider', 'value'),
        Input('reset-filter', 'n_clicks')
    )
    def reset_filters(_):
        return ['All'], [df['Global Index'].min(), df['Global Index'].max()]

    app.run_server(debug=True)


def assign_adjusted_word_indices(df):
    """Assigns 0 as the Adjusted Word Index to words of interest, and adjusts the word indices of surrounding words
    accordingly."""
    stimuli_df = []

    for global_index, current_sentence_df in df.groupby('Global Index'):
        word_of_interest_row = current_sentence_df[current_sentence_df['IsWordOfInterest'] == True]

        if len(word_of_interest_row) > 0:
            word_of_interest_index = next(iter(word_of_interest_row['Word Index']))
            current_sentence_df['Adjusted Word Index'] = current_sentence_df['Word Index'] - word_of_interest_index
        else:
            current_sentence_df['Adjusted Word Index'] = current_sentence_df['Word Index']

        stimuli_df.append(current_sentence_df)

    adjusted_df = pd.concat(stimuli_df)
    return adjusted_df


if __name__ == '__main__':
    main()
