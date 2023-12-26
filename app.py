from viktor import ViktorController
from viktor.core import File
from viktor.parametrization import (
    ViktorParametrization, 
    OptionField,  
    Text, 
    NumberField,
    ActionButton, 
    OptionField,
    LineBreak,
    DownloadButton,
    IntegerField)
from viktor.views import (
    ImageResult, 
    ImageView)
from viktor.result import (
    DownloadResult)
from io import StringIO
import ezbolt


class Parametrization(ViktorParametrization):
    introduction = Text(
        """
# 🔩 Bolt Force Calculations

This app calculates bolt forces in bolt group subjected to shear and in-plane torsion. 
It does so using both the **Elastic Method** and the **Instant Center of Rotation (ICR) method** as outlined in the AISC steel construction manual. 
The ICR method implementation here is based on the work of [Crawford and Kulak (1971).](https://ascelibrary.org/doi/10.1061/JSDEAG.0002844) 
and [Brandt (1982)](https://www.aisc.org/Rapid-Determination-of-Ultimate-Strength-of-Eccentrically-Loaded-Bolt-Groups).
        """)

    text1 = Text("**BOLT GROUP INPUT:**")
    nx = NumberField('$n_x$', min=1, max=20, default=2, description = "Number of bolts along X", flex=25)
    ny = NumberField('$n_y$', min=1, max=20, default=3, description = "Number of bolts along Y", flex=25)
    width = NumberField('Width', min=1, max=100, default=3, suffix="in", description = "Bolt group width with $n_x$ bolts evenly spaced", flex=25)
    height = NumberField('Height', min=1, max=100, default=6, suffix="in", description = "Bolt group height with $n_y$ bolts evenly spaced", flex=25)

    text2 = Text("**APPLIED LOADING INPUT:**")
    Vx = NumberField('$P_x$', min=-1000, max=1000, default=0, suffix="kips", description = "Applied force in the X direction")
    Vy = NumberField('$P_y$', min=-1000, max=1000, default=-50, suffix="kips", description = "Applied force in the Y direction")
    torsion = NumberField('Torsion', min=-100000, max=100000, default=-200, suffix="kip.in", description = "Applied in-plane torsion. You may experience convergence issues for torsion close to 0")
    bolt_capacity = NumberField('Bolt Capacity', min=0.1, max=1000, default=17.9, suffix="kips", description = "Capacity of a single bolt")

    text3 = Text("**DOWNLOAD RESULTS:**")
    button1 = DownloadButton('Download Bolt Force Table - Elastic Method', method='download_elastic', flex=60)
    button2 = DownloadButton('Download Bolt Force Table - ICR Method', method='download_ICR', flex=60)
    disclaimer_text = Text("""This app is for educational use only. Made with [ezbolt.](https://github.com/wcfrobert/ezbolt/). """)







class Controller(ViktorController):
    label = 'Bolt Force Calculation'
    parametrization = Parametrization

    @ImageView("Geometry Preview", duration_guess=10)
    def plot_boltgroup(self, params, **kwargs):
        bolt_group = ezbolt.boltgroup.BoltGroup()
        bolt_group.add_bolts(xo=0, yo=0, width=params.width, height=params.height, nx=params.nx, ny=params.ny)
        fig1 = ezbolt.plotter.preview(bolt_group)
        svg_data = StringIO()
        fig1.savefig(svg_data, format='svg')
        return ImageResult(svg_data)
        

    @ImageView("Elastic Method", duration_guess=10)
    def plot_elastic(self, params, **kwargs):
        bolt_group = ezbolt.boltgroup.BoltGroup()
        bolt_group.add_bolts(xo=0, yo=0, width=params.width, height=params.height, nx=params.nx, ny=params.ny)
        results = bolt_group.solve(Vx=params.Vx, Vy=params.Vy, torsion=params.torsion, bolt_capacity=params.bolt_capacity)
        fig2 = ezbolt.plotter.plot_elastic(bolt_group)
        svg_data = StringIO()
        fig2.savefig(svg_data, format='svg')
        return ImageResult(svg_data)


    @ImageView("ICR Method", duration_guess=10)
    def plot_ICR(self, params, **kwargs):
        bolt_group = ezbolt.boltgroup.BoltGroup()
        bolt_group.add_bolts(xo=0, yo=0, width=params.width, height=params.height, nx=params.nx, ny=params.ny)
        results = bolt_group.solve(Vx=params.Vx, Vy=params.Vy, torsion=params.torsion, bolt_capacity=params.bolt_capacity)
        fig4 = ezbolt.plotter.plot_ICR(bolt_group)
        svg_data = StringIO()
        fig4.savefig(svg_data, format='svg')
        return ImageResult(svg_data)


    def download_elastic(self, params, **kwargs):
        bolt_group = ezbolt.boltgroup.BoltGroup()
        bolt_group.add_bolts(xo=0, yo=0, width=params.width, height=params.height, nx=params.nx, ny=params.ny)
        results = bolt_group.solve(Vx=params.Vx, Vy=params.Vy, torsion=params.torsion, bolt_capacity=params.bolt_capacity)
        df = results["Elastic Method - Superposition"]["Bolt Force Table"]
        return DownloadResult(df.to_csv(), file_name='bolt_force_elastic.csv')


    def download_ICR(self, params, **kwargs):
        bolt_group = ezbolt.boltgroup.BoltGroup()
        bolt_group.add_bolts(xo=0, yo=0, width=params.width, height=params.height, nx=params.nx, ny=params.ny)
        results = bolt_group.solve(Vx=params.Vx, Vy=params.Vy, torsion=params.torsion, bolt_capacity=params.bolt_capacity)
        df = results["Instant Center of Rotation Method"]["Bolt Force Tables"][-1]
        return DownloadResult(df.to_csv(), file_name='bolt_force_ICR.csv')



    
    
    
    
    
    
    


    
