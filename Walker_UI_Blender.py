import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty, CollectionProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel


class WLK_UI_Root_New(Operator):

    bl_idname = "wlk_ui_root.new"
    bl_label = "Add root bone"

    def execute(self, context):

        boneName = bpy.context.selected_pose_bones_from_active_object[-1].name

        if context.scene.wlk_ui_root != boneName:
            context.scene.wlk_ui_root = boneName

        return{'FINISHED'}


#####################################################
##
## WALKS UI LIST

class WLK_UI_UL_Walks_List(PropertyGroup):

    walkName: StringProperty(
           name="Name",
           description="Walk Name",
           default="My Walk")

    actionName: StringProperty(
           name="Cycle Action Name",
           description="Cycle Action Name",
           default="")

    pathName: StringProperty(
           name="Path Name",
           description="Path Name",
           default="")

    floorName: StringProperty(
           name="Floor Name",
           description="Floor Name",
           default="")

    startFrame: IntProperty(
           name="Start Frame",
           description="Start Frame",
           default=0)
    
    repeat: IntProperty(
           name="Repeat Cycle",
           description="Repeat Cycle",
           default=1,
           soft_min=1)

class WLK_UI_UL_Walks(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            text = item.walkName if item.walkName else ' '
            layout.label(text=text)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

class WLK_UI_OT_Walks_New(Operator):

    bl_idname = "wlk_ui_ul_walks_list.new"
    bl_label = "Add a new item"

    def execute(self, context):

        context.scene.wlk_ui_ul_walks_list.add()
        context.scene.wlk_ui_ul_walks_list_index = len(context.scene.wlk_ui_ul_walks_list)-1

        return{'FINISHED'}

class WLK_UI_OT_Walks_Delete(Operator):

    bl_idname = "wlk_ui_ul_walks_list.delete"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.wlk_ui_ul_walks_list

    def execute(self, context):
        myList = context.scene.wlk_ui_ul_walks_list
        index = context.scene.wlk_ui_ul_walks_list_index

        myList.remove(index)
        context.scene.wlk_ui_ul_walks_list_index = min(max(0, index - 1), len(myList) - 1)

        return{'FINISHED'}

class WLK_UI_OT_Walks_Move(Operator):

    bl_idname = "wlk_ui_ul_walks_list.move"
    bl_label = "Move an item in the list"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        return context.scene.wlk_ui_ul_walks_list

    def move_index(self):
        """ Move index of an item render queue while clamping it. """

        index = bpy.context.scene.wlk_ui_ul_walks_list_index
        list_length = len(bpy.context.scene.wlk_ui_ul_walks_list) - 1  # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)

        bpy.context.scene.wlk_ui_ul_walks_list_index = max(0, min(new_index, list_length))

    def execute(self, context):
        wlk_ui_ul_walks_list = context.scene.wlk_ui_ul_walks_list
        index = context.scene.wlk_ui_ul_walks_list_index

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        wlk_ui_ul_walks_list.move(neighbor, index)
        self.move_index()

        return{'FINISHED'}


## WALK UI LIST
##
#######################################################


##################################################################
##
## FEET UI LIST

class WLK_UI_UL_Feet_List(PropertyGroup):

    footName: StringProperty(
           name="Foot Name",
           description="Control for foot",
           default=" ")

class WLK_UI_UL_Feet(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            text = item.footName if item.footName else ' '
            layout.label(text=text)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

class WLK_UI_OT_Feet_New(Operator):

    bl_idname = "wlk_ui_ul_feet_list.new"
    bl_label = "Add a new item"

    def execute(self, context):

        myList = context.scene.wlk_ui_ul_feet_list
        activeBones = bpy.context.selected_pose_bones_from_active_object

        for bone in activeBones:
            isExists = False
            for item in myList:
                if bone.name == item.footName:
                    isExists = True
            if isExists == False:
                myList.add()
                myList[-1].footName = bone.name

        return{'FINISHED'}

class WLK_UI_OT_Feet_Delete(Operator):

    bl_idname = "wlk_ui_ul_feet_list.delete"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.wlk_ui_ul_feet_list

    def execute(self, context):
        wlk_ui_ul_feet_list = context.scene.wlk_ui_ul_feet_list
        index = context.scene.wlk_ui_ul_feet_list_index

        wlk_ui_ul_feet_list.remove(index)
        context.scene.wlk_ui_ul_feet_list_index = min(max(0, index - 1), len(wlk_ui_ul_feet_list) - 1)

        return{'FINISHED'}

class WLK_UI_OT_Feet_Move(Operator):

    bl_idname = "wlk_ui_ul_feet_list.move"
    bl_label = "Move an item in the list"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        return context.scene.wlk_ui_ul_feet_list

    def move_index(self):
        """ Move index of an item render queue while clamping it. """

        index = bpy.context.scene.wlk_ui_ul_feet_list_index
        list_length = len(bpy.context.scene.wlk_ui_ul_feet_list) - 1  # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)

        bpy.context.scene.wlk_ui_ul_feet_list_index = max(0, min(new_index, list_length))

    def execute(self, context):
        wlk_ui_ul_feet_list = context.scene.wlk_ui_ul_feet_list
        index = context.scene.wlk_ui_ul_feet_list_index

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        wlk_ui_ul_feet_list.move(neighbor, index)
        self.move_index()

        return{'FINISHED'}

## FEET UI LIST
##
#######################################################


#######################################################
##
## PANELS

class WLK_Panels:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Walker"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class WLK_PT_Config(WLK_Panels, bpy.types.Panel):
    bl_label = "Config Rig"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        activeObj = bpy.context.active_object
        activeBones = bpy.context.selected_pose_bones_from_active_object

        if activeObj.type != 'ARMATURE':
            layout.label(text="Must select armature object.", icon="ERROR")
            return False

        layout.label(text=activeObj.name, icon="ARMATURE_DATA")

        
        layout.label(text="Root:")
        row = layout.row()
        row.prop(scene, "wlk_ui_root", text="")
        col = row.column(align=True)
        if activeBones is None:
            col.enabled=False
        else:
            if len(activeBones) == 0:
                col.enabled=False
        col.operator('wlk_ui_root.new', text='Add Selected', icon='ADD')


        layout.label(text="Feet:")
        row = layout.row()
        row.template_list("WLK_UI_UL_Feet", "Feet", scene,"wlk_ui_ul_feet_list", scene, "wlk_ui_ul_feet_list_index", rows = 4)
        col = row.column(align=True)
        col.operator('wlk_ui_ul_feet_list.delete', text='', icon='REMOVE')
        col.separator()
        col.operator('wlk_ui_ul_feet_list.move', text='', icon='TRIA_UP').direction = 'UP'
        col.operator('wlk_ui_ul_feet_list.move', text='', icon='TRIA_DOWN').direction = 'DOWN'
        

        row = layout.row()
        if activeBones is None:
            row.enabled=False
        else:
            if len(activeBones) == 0:
                row.enabled=False
        row.operator('wlk_ui_ul_feet_list.new', text='Add Selected', icon='ADD')

        layout.separator()



class WLK_PT_Walks(WLK_Panels, bpy.types.Panel):
    bl_label = "Walks"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        activeObj = bpy.context.active_object

        row = layout.row()
        row.template_list("WLK_UI_UL_Walks", "Walks", scene,"wlk_ui_ul_walks_list", scene, "wlk_ui_ul_walks_list_index", rows = 4)
        col = row.column(align=True)
        col.operator('wlk_ui_ul_walks_list.new', text='', icon='ADD')
        col.operator('wlk_ui_ul_walks_list.delete', text='', icon='REMOVE')
        col.separator()
        col.operator('wlk_ui_ul_walks_list.move', text='', icon='TRIA_UP').direction = 'UP'
        col.operator('wlk_ui_ul_walks_list.move', text='', icon='TRIA_DOWN').direction = 'DOWN'
        if scene.wlk_ui_ul_walks_list_index >=0:
            item = scene.wlk_ui_ul_walks_list[scene.wlk_ui_ul_walks_list_index]
            row = layout.row()
            row.prop(item, "walkName")
            row = layout.row()
            row.prop_search(item, "actionName", bpy.data, "actions", text="Cycle")
            row = layout.row()
            row.prop(item, "startFrame")
            row = layout.row()
            row.prop(item, "repeat")
            row = layout.row()
            row.prop_search(item, "pathName", bpy.data, "curves", text="Path")
            row = layout.row()
            row.prop_search(item, "floorName", bpy.data, "objects", text="Floor")
            layout.separator()
            row = layout.row()
            row.scale_y = 2
            row.operator("object.wlk_analyze_walk_cycle")


## PANELS
##
##########################################################


def register():
    bpy.utils.register_class(WLK_PT_Config)
    bpy.utils.register_class(WLK_PT_Walks)
    bpy.utils.register_class(WLK_UI_Root_New)
    bpy.utils.register_class(WLK_UI_UL_Feet_List)
    bpy.utils.register_class(WLK_UI_UL_Feet)
    bpy.utils.register_class(WLK_UI_OT_Feet_New)
    bpy.utils.register_class(WLK_UI_OT_Feet_Delete)
    bpy.utils.register_class(WLK_UI_OT_Feet_Move)
    bpy.utils.register_class(WLK_UI_UL_Walks_List)
    bpy.utils.register_class(WLK_UI_UL_Walks)
    bpy.utils.register_class(WLK_UI_OT_Walks_New)
    bpy.utils.register_class(WLK_UI_OT_Walks_Delete)
    bpy.utils.register_class(WLK_UI_OT_Walks_Move)

    bpy.types.Scene.wlk_ui_root = bpy.props.StringProperty()
    bpy.types.Scene.wlk_ui_ul_feet_list = CollectionProperty(type = WLK_UI_UL_Feet_List)
    bpy.types.Scene.wlk_ui_ul_feet_list_index = IntProperty(name = "Index for wlk_ui_ul_feet_list",default = 0)
    bpy.types.Scene.wlk_ui_ul_walks_list = CollectionProperty(type = WLK_UI_UL_Walks_List)
    bpy.types.Scene.wlk_ui_ul_walks_list_index = IntProperty(name = "Index for wlk_ui_ul_walks_list",default = 0)

def unregister():
    bpy.utils.unregister_class(WLK_PT_Config)
    bpy.utils.unregister_class(WLK_PT_Walks)
    bpy.utils.unregister_class(WLK_UI_Root_New)
    bpy.utils.unregister_class(WLK_UI_UL_Feet_List)
    bpy.utils.unregister_class(WLK_UI_UL_Feet)
    bpy.utils.unregister_class(WLK_UI_OT_Feet_New)
    bpy.utils.unregister_class(WLK_UI_OT_Feet_Delete)
    bpy.utils.unregister_class(WLK_UI_OT_Feet_Move)
    bpy.utils.unregister_class(WLK_UI_UL_Walks_List)
    bpy.utils.unregister_class(WLK_UI_UL_Walks)
    bpy.utils.unregister_class(WLK_UI_OT_Walks_New)
    bpy.utils.unregister_class(WLK_UI_OT_Walks_Delete)
    bpy.utils.unregister_class(WLK_UI_OT_Walks_Move)

    del bpy.types.Scene.wlk_ui_root
    del bpy.types.Scene.wlk_ui_ul_feet_list
    del bpy.types.Scene.wlk_ui_ul_feet_list_index
    del bpy.types.Scene.wlk_ui_ul_walks_list
    del bpy.types.Scene.wlk_ui_ul_walks_list_index


if __name__ == "__main__":
    register()

