import bpy
from . import PrintTable

WLK = {}
WLK['wlk01'] = {}
WLK['wlk01']['rig_name'] = 'rig'
WLK['wlk01']['hlp_rig'] = 'WLK_HLP_'+'rig'
WLK['wlk01']['hlp_action'] = 'WLK_HLP_'+'rig'
WLK['wlk01']['wlk_action'] = 'WLK_ACTION_'+'rig'

WLK['wlk01']['source_action'] = 'Walk01'
WLK['wlk01']['source_action_repeat'] = 3
WLK['wlk01']['path'] = 'WLK_PATH'

WLK['wlk01']['bones_root'] = 'root'

WLK['wlk01']['bones_feet'] = {}
WLK['wlk01']['bones_feet']['foot_ik.L'] = {}
WLK['wlk01']['bones_feet']['foot_ik.L']['floor_height'] = 0
WLK['wlk01']['bones_feet']['foot_ik.R'] = {}
WLK['wlk01']['bones_feet']['foot_ik.R']['floor_height'] = 0

WLK['wlk01']['bones_feet']['foot_ik.L']['frames_data'] = []
WLK['wlk01']['bones_feet']['foot_ik.R']['frames_data'] = []

WLK['wlk01']['bones_feet']['foot_ik.L']['loc'] = []
WLK['wlk01']['bones_feet']['foot_ik.R']['loc'] = []

WLK['wlk01']['data'] = []

# GET ACTION DURATION
def get_actionDuration(action_name):
    action = bpy.data.actions[action_name]
    duration = action.frame_range[1]-action.frame_range[0]
    return duration

# FIND FCURVE
def get_fCurveByDPathAndArrayIndex(action_name, dataPath, arrayIndex):
    found = None
    for fcurve in bpy.data.actions[action_name].fcurves:     
        if fcurve.data_path == dataPath and fcurve.array_index == arrayIndex:
            found = fcurve
    if found == None:
        print("Get foot fCurve by array index", "WARNING: FCurve not found!", action_name, dataPath, arrayIndex)
    return found  

# GET MARK AT FRAME
def get_footData_markAtFrame(frame, durration, fCurve_upDown, floor_height):
    foot_height = fCurve_upDown.evaluate(frame)
    prev_foot_height = fCurve_upDown.evaluate(frame-1)
    next_foot_height = fCurve_upDown.evaluate(frame+1)
    if foot_height > floor_height:
        mark = "F"
        if foot_height >= prev_foot_height and foot_height > next_foot_height:
            mark = "FU"
    else:
        mark = "C"
        if frame == 1 or prev_foot_height > floor_height:
            mark = "CS" 
        if frame == durration or next_foot_height > floor_height:
            mark = "CE"
    return mark    

# GET OFFSET PER FRAME
def get_footData_OPF(frame, durration, fCurve_forward):
    foot_loc = fCurve_forward.evaluate(frame)
    prev_foot_loc = fCurve_forward.evaluate(frame-1)
    if frame == 1:
        prev_foot_loc = fCurve_forward.evaluate(durration)# Get last frame
    opf = prev_foot_loc - foot_loc
    return round(opf, 4)

   

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):

        wlk_rig = WLK['wlk01']['rig_name']
        wlk_rig_action = WLK['wlk01']['source_action']
        wlk_feet = WLK['wlk01']['bones_feet']

        WLK['wlk01']['data'] = []

        # Get fCurves
        feet_fCurves = {} # To search for specific feet fCurve just once and to keep it here
        for foot in wlk_feet:
            feet_fCurves[foot] = {}
            loc_data_path = 'pose.bones["'+foot+'"].location'
            feet_fCurves[foot]['loc_Y'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, loc_data_path, 1)
            feet_fCurves[foot]['loc_Z'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, loc_data_path, 2) 

        duration = get_actionDuration(wlk_rig_action)
        f = 1
        while f <= duration:

            tmp_data = {}

            for foot in wlk_feet:

                # Get current mark
                floor_height = WLK['wlk01']['bones_feet'][foot]['floor_height']
                mark = get_footData_markAtFrame(f, duration, feet_fCurves[foot]['loc_Z'], floor_height)

                opf = 0
                if mark == "C" or mark == "CE":
                    # Get OPF value
                    opf = get_footData_OPF(f, duration, feet_fCurves[foot]['loc_Y'])
            
                tmp_data[foot]={"mark":mark, "opf":opf}

            WLK['wlk01']['data'].append( dict(tmp_data) )
            tmp_data.clear()

            f += 1

        PrintTable.print_table(WLK['wlk01']['data'], ["CS","FU"])

        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)
    

def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()