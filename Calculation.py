import bpy
import math


a = [(1,2),(3,5),(5,6),(7,8)]
b = [1,3,3,45,4,5,3,345,5,4,2,0,4,3,3,2,1,2,43,5]

def main(context):
    print ("uspeo si svaka cast")
    print (a[1][1])
    print ("test niz")
    #x = b.index(3)
    indexes = [i for i,x in enumerate(b) if x <= 0]
    print (indexes)

x1 = 10
y1 = 0
x2 = 25
y2 =0

def pozicija(context):
    #lista u kom smestamo lokaciju
    z = []
    x = []
    #uzimamo duzinu akcije
    frameRange = int(bpy.data.actions['CubeDance'].frame_range[1])
    cube=bpy.data.objects['Cube']
    print (frameRange)
    #iteracija kroz frejmove i uzimanje lokacije
    for frame in range(0,frameRange):
        bpy.context.scene.frame_set(frame)
        #ver = cube.location.z
        #hor = cube.location.x
        #sid = 
        z.append(lokacija_z)
        x.append(lokacija_x)

    print ("z je")
    print (z)
    print ("x je")
    print (x)
    

#funkcija za izracunavanje duzinu koraka
def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #dist = math.hypot(x2 - x1, y2 - y1)
    print (dist)
    return dist



class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        distance(x1,y1,x2,y2)
        pozicija(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()