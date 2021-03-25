import bpy


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Walker"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)



class PanelOne(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_1"
    bl_label = "Panel One"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Small Classssss")
        # layout.prop_search(scene, "walkCycle", bpy.data, "actions", text="Action")
        layout.operator("object.simple_operator")


class PanelTwo(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_2"
    bl_label = "Panel Two"

    def draw(self, context):
        self.layout.label(text="Also Small Class")


def register():
    bpy.utils.register_class(PanelOne)
    bpy.utils.register_class(PanelTwo)

    # bpy.types.Scene.wlk_rig = bpy.props.StringProperty()
    # bpy.types.Scene.wlk_walkCycle = bpy.props.StringProperty()

def unregister():
    bpy.utils.unregister_class(PanelOne)
    bpy.utils.unregister_class(PanelTwo)

    # del bpy.types.Scene.walkCycle


if __name__ == "__main__":
    register()

