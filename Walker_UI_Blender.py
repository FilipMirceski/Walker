import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty, CollectionProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel

class ListItem(PropertyGroup):

    foot: StringProperty(
           name="Foot",
           description="Control for foot",
           default=" ")

    axisFront: EnumProperty(
           name="Front Axis",
           description="Set Front Axis Direction",
           items=   (('X', 'X', 'X'),  
                    ('Y', 'Y', 'Y'),  
                    ('Z', 'Z', 'Z'),
                    ('-X', '-X', '-X'),  
                    ('-Y', '-Y', '-Y'),  
                    ('-Z', '-Z', '-Z')),
            default='-Y'
           )

    axisUp: EnumProperty(
           name="Up Axis",
           description="Set Up Axis Direction",
           items=   (('X', 'X', 'X'),  
                    ('Y', 'Y', 'Y'),  
                    ('Z', 'Z', 'Z'),
                    ('-X', '-X', '-X'),  
                    ('-Y', '-Y', '-Y'),  
                    ('-Z', '-Z', '-Z')),
            default='Z'
           )
    
    contactHeight: FloatProperty(
           name="Contact Height",
           description="",
           default=0.0)

    useFoot: BoolProperty(
           name="Use",
           description="Use foot in sims",
           options=set(),
           default=True)

class MY_UL_List(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'BONE_DATA'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            text = item.foot if item.foot else ' '
            layout.label(text=text, icon = custom_icon)
            icon = 'CHECKBOX_HLT' if item.useFoot else 'CHECKBOX_DEHLT'
            layout.prop(item, "useFoot", text="", icon=icon, emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

class LIST_OT_NewItem(Operator):

    bl_idname = "my_list.new_item"
    bl_label = "Add a new item"

    def execute(self, context):
        context.scene.my_list.add()

        return{'FINISHED'}

class LIST_OT_DeleteItem(Operator):

    bl_idname = "my_list.delete_item"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.my_list

    def execute(self, context):
        my_list = context.scene.my_list
        index = context.scene.list_index

        my_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(my_list) - 1)

        return{'FINISHED'}

class LIST_OT_MoveItem(Operator):

    bl_idname = "my_list.move_item"
    bl_label = "Move an item in the list"

    direction = bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        return context.scene.my_list

    def move_index(self):
        """ Move index of an item render queue while clamping it. """

        index = bpy.context.scene.list_index
        list_length = len(bpy.context.scene.my_list) - 1  # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)

        bpy.context.scene.list_index = max(0, min(new_index, list_length))

    def execute(self, context):
        my_list = context.scene.my_list
        index = context.scene.list_index

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        my_list.move(neighbor, index)
        self.move_index()

        return{'FINISHED'}

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Walker"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class PanelOne(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_1"
    bl_label = "Params"

    def updateVar(self, value):
        bpy.context.scene.wlk_targetArmature_prev = value

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop_search(scene, "wlk_targetArmature", bpy.data, "armatures", text="Armature")
        layout.prop_search(scene, "wlk_targetAction", bpy.data, "actions", text="Action")

        layout.prop_search(scene, "wlk_root", bpy.data.armatures[scene.wlk_targetArmature], "bones", text="Root")

        layout.label(text="Feet:")

        row = layout.row()
        row.template_list("MY_UL_List", "The_List", scene,"my_list", scene, "list_index", rows = 2)

        col = row.column(align=True)
        col.operator('my_list.new_item', text='', icon='ADD')
        col.operator('my_list.delete_item', text='', icon='REMOVE')
        col.separator()
        col.operator('my_list.move_item', text='', icon='TRIA_UP')
        col.operator('my_list.move_item', text='', icon='TRIA_DOWN')

        if scene.list_index >= 0 and scene.my_list:
            item = scene.my_list[scene.list_index]
            row = layout.row()
            row.prop_search(item, "foot", bpy.data.armatures[scene.wlk_targetArmature], "bones", text="Foot")
            row.prop(item, "useFoot")
            layout.prop(item, "axisFront")
            layout.prop(item, "axisUp")
            layout.prop(item, "contactHeight")

        layout.separator()



class PanelTwo(View3DPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_test_2"
    bl_label = "Tests"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("object.wlk_analyze_armature")
        layout.operator("object.wlk_analyze_walk_cycle")

def update_targetArmature(self, context):
    print("CHANGED")
    terms = ["root", "foot_ik.l", "foot_ik.r"]
    targetArmature = bpy.data.armatures[bpy.context.scene.wlk_targetArmature]
    # Find bones with matching name
    matching = []
    for bone in targetArmature.bones:
        for term in terms:
            if term in bone.name.lower():
                matching.append(bone.name)
    # Remove old 
    i = len(bpy.context.scene.my_list)
    while i >= 0:
        bpy.context.scene.my_list.remove(i)
        i-=1
    bpy.context.scene.list_index = 0
    # Create new
    for item in matching:
        if "root" in item:
            bpy.context.scene.wlk_root = item
        if "foot" in item:
            bpy.context.scene.my_list.add()
            bpy.context.scene.my_list[-1].foot = item


def register():
    bpy.utils.register_class(PanelOne)
    bpy.utils.register_class(PanelTwo)
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(MY_UL_List)
    bpy.utils.register_class(LIST_OT_NewItem)
    bpy.utils.register_class(LIST_OT_DeleteItem)
    bpy.utils.register_class(LIST_OT_MoveItem)

    bpy.types.Scene.wlk_targetArmature = bpy.props.StringProperty(update=update_targetArmature)
    bpy.types.Scene.wlk_targetAction = bpy.props.StringProperty()
    bpy.types.Scene.wlk_root = bpy.props.StringProperty()

    bpy.types.Scene.my_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list",default = 0)

def unregister():
    bpy.utils.unregister_class(PanelOne)
    bpy.utils.unregister_class(PanelTwo)
    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(MY_UL_List)
    bpy.utils.unregister_class(LIST_OT_NewItem)
    bpy.utils.unregister_class(LIST_OT_DeleteItem)
    bpy.utils.unregister_class(LIST_OT_MoveItem)

    del bpy.types.Scene.wlk_targetArmature
    del bpy.types.Scene.wlk_targetAction
    del bpy.types.Scene.wlk_root
    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index


if __name__ == "__main__":
    register()

