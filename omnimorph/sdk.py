# omnimorph/sdk.py
from .dy_methods import DynamicMethodGenerator
from .dy_converter import DynamicConverter

class Omnimorph(DynamicMethodGenerator, DynamicConverter):
    def __init__(self, obj):
        DynamicMethodGenerator.__init__(self, obj)
        DynamicConverter.__init__(self, obj)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    class Human:
        def __init__(self, mass, height):
            self.mass = mass
            self.height = height

    human = Human(80, 1.75)
    om_human = Omnimorph(human)
    print("Is heavy:", om_human.is_heavy(threshold=20.0))


    class KlamptGeometry:
        def __init__(self):
            self.vertices = [(0,0,0), (1,0,0), (0,1,0)]
            self.faces = [(0,1,2)]
        def getVertices(self):
            return self.vertices
        def getFaces(self):
            return self.faces

    klamp_geom = KlamptGeometry()
    om_klamp = Omnimorph(klamp_geom)
    open3d_obj = om_klamp.to('open3d')
    print("Converted object:", open3d_obj)
