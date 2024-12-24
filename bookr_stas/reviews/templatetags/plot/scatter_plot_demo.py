from plotly.offline import plot
import plotly.graph_objs as graphs


def generate_scatter_plot():
    figure = graphs.Figure()
    scatter = graphs.Scatter(x=[1, 2, 3, 4, 5], y=[3, 8, 7, 9, 2])
    figure.add_trace(scatter)
    return plot(figure, output_type='file')


#     plot_html = plot(figure, output_type='file')
#     html_content = f'<html><head><title>Plot Demo</title></head><body>{plot_html}</body></html>'
#     try:
#         with open('plot_demo.html', 'w') as plot_file:
#             plot_file.write(html_content)
#     except (IOError, OSError) as file_io_error:
#         print(f'Unable to generate plot file. Exception: {file_io_error}')
#
#
# if __name__ == '__main__':
#     generate_scatter_plot()
