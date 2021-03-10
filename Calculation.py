import bpy
import math

wlk_collection = 'Novi Test'


def main(context):
    print("")
    print("")
    print("################################## WLK: INIT")
    print("")

def new_collection(name):
    
    collection = bpy.data.collections.get( name )
    if collection == None:
        collection = bpy.data.collections.new( name )
        
    if bpy.context.scene.collection.children.get( collection.name ) == None:
        bpy.context.scene.collection.children.link( collection )
        
    print('Create new collection', name)
   
    return collection

 #new_collection(wlk_collection)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        new_collection(wlk_collection)
        
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)
    

def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()