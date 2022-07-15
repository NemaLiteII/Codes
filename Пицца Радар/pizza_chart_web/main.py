from flask import Flask, redirect
from flask import request
import io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.transforms import Affine2D
from matplotlib.ticker import FixedLocator
from matplotlib.spines import Spine
from matplotlib.path import Path
from math import pi

from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

@app.route("/")
def index():
    return (
        """<meta charset="utf-8">
        <title>Pizza-chart!</title>
	<style>
		input::-webkit-outer-spin-button,
		input::-webkit-inner-spin-button 
			{
			-webkit-appearance: none;
			margin: 0;
			}
		body 	{
			margin: 5% 20% 5% 20%;
            		background-color: #6C3483; /* Цвет фона веб-страницы */
           		}
		table 	{
			background-color: #00ccff; /* Цвет фона веб-страницы */
            		font: 16pt Coco; /* Шрифт */
           		border: 2px solid black; /* Параметры рамки */
            		padding: 2%; /* Поля вокруг текста */
            		margin-top: 5%;
			margin-bottom: 5%;
			margin-left: auto;
  			margin-right: auto;
			}
           	div	{
            		font: 16pt Coco; /* Шрифт */
           		#border: 1px solid black; /* Параметры рамки */
            		padding: 1.5%; /* Поля вокруг текста */
           		}
		td { width: 80%; }
		#input { width: 20%; padding-left: 5%;}
		input[type="number"] {
   			width: 80%;
    			height: 34px;
    			padding-left: 25%;
    			font-size: 26px;
			color: black;
    			background-color: yellow;
    			border: 2px solid purple;
    			border-radius: 16px;
			}
           	h1 { text-align: center; }
	</style>
	<body>
		<form action="/plot" method="get" target="_blank">
		<table>
        		<tr>
				<td>Дисконтирование устаревших решений:</td>
				<td id=input><input type="number" name="1" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
			</tr>
        		<tr>
				<td>Давление на независимого партнера:</td>
				<td id=input><input type="number" name="2" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
        		</tr>
        		<tr>
				<td>Конструирование компаний:</td>
				<td id=input><input type="number" name="3" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
			</tr>
        		<tr>
				<td>Препарирование технологий:</td>
				<td id=input><input type="number" name="4" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
			</tr>
        		<tr>
				<td>Скрининг шансов:</td>
				<td id=input><input type="number" name="5" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
			</tr>
        		<tr>
				<td>Борьба за привилегии:</td>
				<td id=input><input type="number" name="6" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
			</tr>
        		<tr>
				<td>Фиктивная деятельность:</td>
				<td id=input><input type="number" name="7" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
			</tr>
        		<tr>
				<td>Отношения вместо дела:</td>
				<td id=input><input type="number" name="8" autocomplete="off"/
				oninput="this.value = this.value>10 ? 10 : (this.value)"></td>
			</tr>
		</table>
		<h1><input type="submit" value="Convert to Pizza" style="text-align:center; background-color: orange; font: 18pt Coco;
			height:50px; width:200px; border: 3px solid #3498DB; border-radius: 16px;"><h1>
		</form>
		<iframe src="https://giphy.com/embed/MWSRkVoNaC30A" width="342" height="412" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
		<iframe src="https://giphy.com/embed/nR4L10XlJcSeQ" width="480" height="412" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
	</body>"""
    )

@app.route("/plot")
def plot():
    cols = [request.args.get(f"{i}", "") for i in range(1,9)]
    cols = [col if col else 0 for col in cols]
    return redirect(('/plot'+'/{}'*8+'/pizza').format(*cols))

@app.route("/plot/<int:col_1>/<int:col_2>/<int:col_3>/<int:col_4>/<int:col_5>/<int:col_6>/<int:col_7>/<int:col_8>/<file_name>")
def web1(col_1=0, col_2=0, col_3=0, col_4=0, col_5=0, col_6=0, col_7=0, col_8=0, file_name='PizzaChart.png'):
    #file_name='123.png'
    numbers= [col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8]
    print(numbers)
    col1 = 'Дисконтирование\nустаревших\nрешений'
    col2 = 'Давление на\nнезависимого\nпартнера'
    col3 = 'Конструирование\n компаний'
    col4 = 'Препарирование\nтехнологий'
    col5 = 'Скрининг\nшансов'
    col6 = 'Борьба за\nпривилегии'
    col7 = 'Фиктивная\nдеятельность'
    col8 = 'Отношения\nвместо дела'
    dict1 = {col: 0 for col in [col1, col2, col3, col4, col5, col6, col7, col8]}
    N = 8
    theta = radar_factory(8, frame='polygon')

    angles = np.linspace(0, 2 * pi, N, endpoint=False)
    angles_mids = angles + (angles[1] / 2)

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(left=0)
    ax.xaxis.set_minor_locator(FixedLocator(angles))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    plt.ylim([0, 10])

    ax.set_theta_offset(pi/8-pi/4)
    ax.set_theta_direction(1)
    ax.set_xticks(angles_mids)
    ax.set_xticklabels(dict1.keys())
    ax.grid(True, axis='x', which='minor')
    ax.grid(False, axis='x', which='major')
    ax.grid(True, axis='y', which='major')
    ax.set_rgrids([2,4,6,8,10], [])
    #ax.set_title(file_name,  position=(0.5, 1.1), ha='center')
    color1='springgreen'
    color2='seagreen'
    color3='tomato'
    color4='red'
    for i in range(6):
        ax.fill_between(angles[i:i+2], 0, numbers[i] , facecolor=color1, edgecolor=color2, linewidth=2)
    ax.fill_between(angles[5:7], 0, numbers[5], facecolor=color3, edgecolor=color4, linewidth=2)
    ax.fill_between(angles[6:8], 0, numbers[6], facecolor=color3, edgecolor=color4, linewidth=2)
    ax.fill_between([angles[7],(angles[7]+angles[1])], 0, numbers[7], facecolor=color3, edgecolor=color4, linewidth=2)

    gridlines = ax.yaxis.get_gridlines()
    for gl in gridlines:
        gl.get_path()._interpolation_steps = 8
        
    for index, label in enumerate(ax.get_xticklabels()):
        label.set_weight("bold")
        label.set_fontsize(14)
        if index in [0, 1, 7]:
            label.set_horizontalalignment("left")
        elif index in [3, 4, 5]:
            label.set_horizontalalignment("right")

    
    #plt.savefig(os.path.join(uploads_dir, secure_filename(file_name)), transparent=True)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def radar_factory(num_vars, frame='circle'):
    
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    
    class RadarAxes(PolarAxes):
        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return Circle((0.5, 0.5), 0.5)
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                spine.set_transform(Affine2D().rotate(pi/8).scale(0.5).translate(.5, .5)
                                    + self.transAxes)

                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
