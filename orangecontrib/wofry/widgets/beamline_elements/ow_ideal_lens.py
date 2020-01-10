import numpy
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from syned.beamline.optical_elements.ideal_elements.lens import IdealLens

from wofry.beamline.optical_elements.ideal_elements.lens import WOIdealLens

from orangecontrib.wofry.widgets.gui.ow_optical_element import OWWOOpticalElement


class OWWOIdealLens(OWWOOpticalElement):

    name = "Ideal Lens"
    description = "Wofry: Ideal Lens"
    icon = "icons/ideal_lens.png"
    priority = 43

    focal_x = Setting(1.0)
    focal_y = Setting(1.0)

    def __init__(self):
        super().__init__()

    def draw_specific_box(self):

        self.filter_box = oasysgui.widgetBox(self.tab_bas, "Ideal Lens Setting", addSpace=True, orientation="vertical")

        oasysgui.lineEdit(self.filter_box, self, "focal_x", "Horizontal Focal Length [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.filter_box, self, "focal_y", "Vertical Focal Length [m]", labelWidth=260, valueType=float, orientation="horizontal")


    def get_optical_element(self):
        return WOIdealLens(name=self.oe_name,
                           focal_x=self.focal_x,
                           focal_y=self.focal_y)

    def get_optical_element_python_code(self):
        txt  = ""
        txt += "\nfrom wofry.beamline.optical_elements.ideal_elements.lens import WOIdealLens"
        txt += "\n"
        txt += "\noptical_element = WOIdealLens(name='%s',focal_x=%f,focal_y=%f)"%(self.oe_name,self.focal_x,self.focal_y)
        txt += "\n"
        return txt

    def check_data(self):
        super().check_data()

        congruence.checkStrictlyPositiveNumber(numpy.abs(self.focal_x), "Horizontal Focal Length")
        congruence.checkStrictlyPositiveNumber(numpy.abs(self.focal_y), "Vertical Focal Length")

    def receive_specific_syned_data(self, optical_element):
        if not optical_element is None:
            if isinstance(optical_element, IdealLens):
                self.focal_x = optical_element._focal_x
                self.focal_y = optical_element._focal_y
            else:
                raise Exception("Syned Data not correct: Optical Element is not a Slit")
        else:
            raise Exception("Syned Data not correct: Empty Optical Element")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from wofry.propagator.wavefront2D.generic_wavefront import GenericWavefront2D

    a = QApplication(sys.argv)
    ow = OWWOIdealLens()
    ow.input_wavefront = GenericWavefront2D.initialize_wavefront_from_range(-0.002,0.002,-0.001,0.001,(400,200))

    ow.show()
    a.exec_()
    ow.saveSettings()
