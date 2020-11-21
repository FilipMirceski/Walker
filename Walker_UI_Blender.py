import bpy


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "New"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class PanelOne(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_1"
    bl_label = "Panel One"

    def draw(self, context):
        self.layout.label(text="Small Class")


class PanelTwo(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_2"
    bl_label = "Panel Two"

    def draw(self, context):
        self.layout.label(text="Also Small Class")


def register():
    bpy.utils.register_class(PanelOne)
    bpy.utils.register_class(PanelTwo)

def unregister():
    bpy.utils.unregister_class(PanelOne)
    bpy.utils.unregister_class(PanelTwo)


if __name__ == "__main__":
    register()

