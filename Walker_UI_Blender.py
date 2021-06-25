import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty, CollectionProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, Bone



#################################################################################
##
## WALKERS PROPERTY GROUP AND OPERATORS


# Walker index not added as Blender property, 
# because it needed to be updated automatically from Panel Class
# (not possible with Blender properties) and
# not necessary to be saved with file
wlk_ot_walkers_index = -1


# Definition for Feet list in Walkers list
class WLK_UL_Walkers_Feet(PropertyGroup):
    footName: StringProperty(name="Foot Name", description="Control for foot", default=" ")


# Definition for Walk list in Walkers list
class WLK_UL_Walkers_Walks(PropertyGroup):
    walkName: StringProperty( name="Name", description="Walk Name", default="My Walk")
    actionName: StringProperty( name="Cycle Action Name", description="Cycle Action Name", default="")
    pathName: StringProperty( name="Path Name", description="Path Name", default="")
    floorName: StringProperty( name="Floor Name", description="Floor Name", default="")
    startFrame: IntProperty( name="Start Frame", description="Start Frame", default=0)
    repeat: IntProperty( name="Repeat Cycle", description="Repeat Cycle", default=1, soft_min=1)


# Definition for Walkers list
class WLK_Walkers(PropertyGroup):
    rigObj: PointerProperty(name="Rig Object", type=bpy.types.Object)
    root: StringProperty(name="Root", description="Root", default="")
    feet: CollectionProperty(type = WLK_UL_Walkers_Feet)
    feet_index: IntProperty(name = "Index for feet", default = -1)
    walks: CollectionProperty(type = WLK_UL_Walkers_Walks)
    walks_index: IntProperty(name = "Index for walks",default = -1)


# Operator to add new Walker to Walkers list
class WLK_OT_Walkers_New(Operator):
    bl_idname = "wlk_ot_walkers.new"
    bl_label = "Add a new Walker"
    def execute(self, context):
        activeObj = bpy.context.active_object
        scene = context.scene
        scene.wlk_walkers.add()
        i = len(scene.wlk_walkers)-1
        scene.wlk_walkers[i].rigObj = activeObj
        return{'FINISHED'}


# Operator to delete Walker from Walkers list
class WLK_OT_Walkers_Del(Operator):
    bl_idname = "wlk_ot_walkers.del"
    bl_label = "Remove a Walker"
    def execute(self, context):
        scene = context.scene
        activeObj = bpy.context.active_object
        myList = scene.wlk_walkers
        global wlk_ot_walkers_index #Use global
        scene.wlk_walkers.remove(wlk_ot_walkers_index)
        return{'FINISHED'}


# Operator to set root bone
class WLK_OT_Walkers_SetRoot(Operator):
    bl_idname = "wlk_ot_walkers.setroot"
    bl_label = "Set root bone"
    def execute(self, context):
        scene = context.scene
        activeObj = bpy.context.active_object
        myList = scene.wlk_walkers
        global wlk_ot_walkers_index #Use global
        boneName = bpy.context.selected_pose_bones_from_active_object[-1].name
        scene.wlk_walkers[wlk_ot_walkers_index].root = boneName
        return{'FINISHED'}


######################################
##
## UI FEET LIST AND OPERATORS


# UI for Feet list
class WLK_UI_UL_Walkers_Feet(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):
        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            text = item.footName if item.footName else ' '
            layout.label(text=text)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")


# Operator to add new Foot to Feet list
class WLK_UI_OT_UL_Walkers_Feet_New(Operator):
    bl_idname = "wlk_ui_ot_ul_walkers_feet.new"
    bl_label = "Add a new item"
    def execute(self, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        feet_list = scene.wlk_walkers[wlk_ot_walkers_index].feet
        feet_index = scene.wlk_walkers[wlk_ot_walkers_index].feet_index
        activeBones = bpy.context.selected_pose_bones_from_active_object
        for bone in activeBones:
            isExists = False
            for item in feet_list:
                if bone.name == item.footName:
                    isExists = True
            if isExists == False:
                feet_list.add()
                feet_list[-1].footName = bone.name
        return{'FINISHED'}


# Operator to delete Foot from Feet list
class WLK_UI_OT_UL_Walkers_Feet_Del(Operator):
    bl_idname = "wlk_ui_ot_ul_walkers_feet.del"
    bl_label = "Deletes an item"
    @classmethod
    def poll(cls, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        feet_list = scene.wlk_walkers[wlk_ot_walkers_index].feet
        return feet_list
    def execute(self, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        feet_list = scene.wlk_walkers[wlk_ot_walkers_index].feet
        feet_index = scene.wlk_walkers[wlk_ot_walkers_index].feet_index
        feet_list.remove(feet_index)
        feet_index = min(max(0, feet_index - 1), len(feet_list) - 1)
        return{'FINISHED'}


# Operator to move place of Foot in Feet list
class WLK_UI_OT_UL_Walkers_Feet_Move(Operator):
    bl_idname = "wlk_ui_ot_ul_walkers_feet.move"
    bl_label = "Move an item in the list"
    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))
    @classmethod
    def poll(cls, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        feet_list = scene.wlk_walkers[wlk_ot_walkers_index].feet
        return feet_list
    def move_index(self):
        scene = bpy.context.scene
        global wlk_ot_walkers_index #Use global
        feet_list = scene.wlk_walkers[wlk_ot_walkers_index].feet
        feet_index = scene.wlk_walkers[wlk_ot_walkers_index].feet_index
        list_length = len(feet_list) - 1  # (index starts at 0)
        new_index = feet_index + (-1 if self.direction == 'UP' else 1)
        feet_index = max(0, min(new_index, list_length))
    def execute(self, context):
        scene = bpy.context.scene
        global wlk_ot_walkers_index #Use global
        feet_list = scene.wlk_walkers[wlk_ot_walkers_index].feet
        feet_index = scene.wlk_walkers[wlk_ot_walkers_index].feet_index
        neighbor = feet_index + (-1 if self.direction == 'UP' else 1)
        feet_list.move(neighbor, feet_index)
        self.move_index()
        return{'FINISHED'}


## UI FEET LIST AND OPERATORS
##
######################################


######################################
##
## UI WALKS LIST AND OPERATORS


# UI for Walks list
class WLK_UI_UL_Walkers_Walks(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):
        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            text = item.walkName if item.walkName else ' '
            layout.label(text=text)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")


# Operator to add new Walk to Walks list
class WLK_UI_OT_UL_Walkers_Walks_New(Operator):
    bl_idname = "wlk_ui_ot_ul_walkers_walks.new"
    bl_label = "Add a new item"
    def execute(self, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        walks_list = scene.wlk_walkers[wlk_ot_walkers_index].walks
        walks_index = scene.wlk_walkers[wlk_ot_walkers_index].walks_index
        walks_list.add()
        walks_index = len(walks_list)-1
        return{'FINISHED'}


# Operator to delete Walk from Walks list
class WLK_UI_OT_UL_Walkers_Walks_Del(Operator):
    bl_idname = "wlk_ui_ot_ul_walkers_walks.del"
    bl_label = "Deletes an item"
    @classmethod
    def poll(cls, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        walks_list = scene.wlk_walkers[wlk_ot_walkers_index].walks
        return walks_list
    def execute(self, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        walks_list = scene.wlk_walkers[wlk_ot_walkers_index].walks
        walks_index = scene.wlk_walkers[wlk_ot_walkers_index].walks_index
        walks_list.remove(walks_index)
        walks_index = min(max(0, walks_index - 1), len(walks_list) - 1)
        return{'FINISHED'}


# Operator to move place of Walk in Walks list
class WLK_UI_OT_UL_Walkers_Walks_Move(Operator):
    bl_idname = "wlk_ui_ot_ul_walkers_walks.move"
    bl_label = "Move an item in the list"
    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))
    @classmethod
    def poll(cls, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        walks_list = scene.wlk_walkers[wlk_ot_walkers_index].walks
        return walks_list
    def move_index(self):
        scene = bpy.context.scene
        global wlk_ot_walkers_index #Use global
        walks_list = scene.wlk_walkers[wlk_ot_walkers_index].walks
        walks_index = scene.wlk_walkers[wlk_ot_walkers_index].walks_index
        list_length = len(walks_list) - 1  # (index starts at 0)
        new_index = walks_index + (-1 if self.direction == 'UP' else 1)
        walks_index = max(0, min(new_index, list_length))

    def execute(self, context):
        scene = context.scene
        global wlk_ot_walkers_index #Use global
        walks_list = scene.wlk_walkers[wlk_ot_walkers_index].walks
        walks_index = scene.wlk_walkers[wlk_ot_walkers_index].walks_index
        neighbor = walks_index + (-1 if self.direction == 'UP' else 1)
        walks_list.move(neighbor, walks_index)
        self.move_index()

        return{'FINISHED'}


## UI WALKS LIST AND OPERATORS
##
######################################


## WALKERS PROPERTY GROUP AND OPERATORS
##
#################################################################################



#################################################################################
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
        activeObj = context.active_object
        activeBones = context.selected_pose_bones_from_active_object

        if activeObj.type != 'ARMATURE': # Return if not active object not armature type
            layout.label(text="Must select armature object.", icon="ERROR")
            return None

        layout.label(text=activeObj.name, icon="ARMATURE_DATA") # Layout active object name

        ################################################## Iterate walkers data to filter active object
        walkers = scene.wlk_walkers # Load walkers configs
        rigFound = False
        walkers_item = None
        global wlk_ot_walkers_index #Use global var
        i = 0
        while i<len(walkers):
            item = walkers[i]
            if item.rigObj == activeObj:# If active object founded
                rigFound = True
                walkers_item = item
                wlk_ot_walkers_index = i
            i += 1

        # If active object not founded return
        row = layout.row()
        row.scale_y = 2
        if rigFound == False:
            row.operator('wlk_ot_walkers.new', text='Add Walker to Rig', icon='ADD')# Option to add walkers data for active object
            wlk_ot_walkers_index = -1
            return None
        # If active object founded
        row.operator('wlk_ot_walkers.del', text='Remove Walker from Rig', icon='REMOVE')# Option to remove walkers data for active object
    
        ######################################################################################## Set ROOT
        layout.label(text="Root:")
        row = layout.row()
        row.prop(walkers_item, "root", text="")
        col = row.column(align=True)
        if activeBones is None:
            col.enabled=False
        else:
            if len(activeBones) == 0:
                col.enabled=False
        col.operator('wlk_ot_walkers.setroot', text='Add Selected', icon='ADD')

        ######################################################################################### Set FEET
        layout.label(text="Feet:")
        row = layout.row()
        row.template_list("WLK_UI_UL_Walkers_Feet", "Feet", walkers_item,"feet", walkers_item, "feet_index", rows = 4)
        col = row.column(align=True)
        col.operator('wlk_ui_ot_ul_walkers_feet.del', text='', icon='REMOVE')
        col.separator()
        col.operator('wlk_ui_ot_ul_walkers_feet.move', text='', icon='TRIA_UP').direction = 'UP'
        col.operator('wlk_ui_ot_ul_walkers_feet.move', text='', icon='TRIA_DOWN').direction = 'DOWN'
        row = layout.row()
        if activeBones is None:
            row.enabled=False
        else:
            if len(activeBones) == 0:
                row.enabled=False
        row.operator('wlk_ui_ot_ul_walkers_feet.new', text='Add Selected', icon='ADD')
        layout.separator()


class WLK_PT_Walks(WLK_Panels, bpy.types.Panel):
    bl_label = "Walks"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        activeObj = context.active_object

        if activeObj.type != 'ARMATURE': # Return if not active object not armature type
            layout.label(text="Must select armature object.", icon="ERROR")
            return None

        # If active object not founded return
        walkers = scene.wlk_walkers
        global wlk_ot_walkers_index #Use global var
        if wlk_ot_walkers_index == -1:
            layout.label(text="Must Add Walker to Rig in Config Rig Panel.", icon="ERROR")
            return None
        
        walkers_item = walkers[wlk_ot_walkers_index]

        # Walks list UI    
        row = layout.row()
        row.template_list("WLK_UI_UL_Walkers_Walks", "Walks", walkers_item,"walks", walkers_item, "walks_index", rows = 4)
        col = row.column(align=True)
        col.operator('wlk_ui_ot_ul_walkers_walks.new', text='', icon='ADD')
        col.operator('wlk_ui_ot_ul_walkers_walks.del', text='', icon='REMOVE')
        col.separator()
        col.operator('wlk_ui_ot_ul_walkers_walks.move', text='', icon='TRIA_UP').direction = 'UP'
        col.operator('wlk_ui_ot_ul_walkers_walks.move', text='', icon='TRIA_DOWN').direction = 'DOWN'

        # Selected walk inputs
        if walkers_item.walks_index >=0:
            item = walkers_item.walks[walkers_item.walks_index]
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
#################################################################################



#################################################################################
##
## REGISTER


def register():

    # Walkers list definition, UI and operators
    bpy.utils.register_class(WLK_UL_Walkers_Feet)
    bpy.utils.register_class(WLK_UL_Walkers_Walks)
    bpy.utils.register_class(WLK_Walkers)
    bpy.utils.register_class(WLK_OT_Walkers_New)
    bpy.utils.register_class(WLK_OT_Walkers_Del)
    bpy.utils.register_class(WLK_OT_Walkers_SetRoot)
    bpy.types.Scene.wlk_walkers = CollectionProperty(type = WLK_Walkers)

    # Feet list UI and operators
    bpy.utils.register_class(WLK_UI_UL_Walkers_Feet)
    bpy.utils.register_class(WLK_UI_OT_UL_Walkers_Feet_New)
    bpy.utils.register_class(WLK_UI_OT_UL_Walkers_Feet_Del)
    bpy.utils.register_class(WLK_UI_OT_UL_Walkers_Feet_Move)

    # Walks list UI and operators
    bpy.utils.register_class(WLK_UI_UL_Walkers_Walks)
    bpy.utils.register_class(WLK_UI_OT_UL_Walkers_Walks_New)
    bpy.utils.register_class(WLK_UI_OT_UL_Walkers_Walks_Del)
    bpy.utils.register_class(WLK_UI_OT_UL_Walkers_Walks_Move)

    # Panels
    bpy.utils.register_class(WLK_PT_Config)
    bpy.utils.register_class(WLK_PT_Walks)


def unregister():

    # Walkers list definition, UI and operatorsbpy.utils.unregister_class(WLK_Walkers)
    bpy.utils.unregister_class(WLK_UL_Walkers_Walks)
    bpy.utils.unregister_class(WLK_UL_Walkers_Feet)
    bpy.utils.unregister_class(WLK_OT_Walkers_New)
    bpy.utils.unregister_class(WLK_OT_Walkers_Del)
    bpy.utils.unregister_class(WLK_OT_Walkers_SetRoot)
    del bpy.types.Scene.wlk_walkers

    # Feet list UI and operators
    bpy.utils.unregister_class(WLK_UI_UL_Walkers_Feet)
    bpy.utils.unregister_class(WLK_UI_OT_UL_Walkers_Feet_New)
    bpy.utils.unregister_class(WLK_UI_OT_UL_Walkers_Feet_Del)
    bpy.utils.unregister_class(WLK_UI_OT_UL_Walkers_Feet_Move)

    # Walks list UI and operators
    bpy.utils.unregister_class(WLK_UI_UL_Walkers_Walks)
    bpy.utils.unregister_class(WLK_UI_OT_UL_Walkers_Walks_New)
    bpy.utils.unregister_class(WLK_UI_OT_UL_Walkers_Walks_Del)
    bpy.utils.unregister_class(WLK_UI_OT_UL_Walkers_Walks_Move)

    # Panels
    bpy.utils.unregister_class(WLK_PT_Config)
    bpy.utils.unregister_class(WLK_PT_Walks)


if __name__ == "__main__":
    register()

