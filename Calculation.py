import bpy




def createmat(context):
    
    a = 5
    b = 3
    c = a + b

    print("Kako si filipe")
    print(c)

    return c


class CreateBSDF(bpy.types.Operator):#create material
    """Tooltip"""
    bl_idname = "object.createbsdf"
    bl_label = "Create Principled BSDF"

    #@classmethod
    #def poll(cls, context):
    #    return context.active_object is not None

    def execute(self, context):
        createmat(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CreateBSDF)


def unregister():
    bpy.utils.unregister_class(CreateBSDF)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()
