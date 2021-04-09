import bpy
from . import PrintTable
from mathutils import Vector, Quaternion

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
WLK['wlk01']['bones_feet']['foot_ik.L']['frames_data'] = []
WLK['wlk01']['bones_feet']['foot_ik.L']['loc'] = []

WLK['wlk01']['bones_feet']['foot_ik.R'] = {}
WLK['wlk01']['bones_feet']['foot_ik.R']['floor_height'] = 0
WLK['wlk01']['bones_feet']['foot_ik.R']['frames_data'] = []
WLK['wlk01']['bones_feet']['foot_ik.R']['loc'] = []

WLK['wlk01']['walk_cycle_data'] = []


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
def get_markAtFrame(frame, durration, fCurve_upDown, floor_height):
    foot_height = fCurve_upDown.evaluate(frame)
    prev_foot_height = fCurve_upDown.evaluate(frame-1)
    next_foot_height = fCurve_upDown.evaluate(frame+1)
    if foot_height > floor_height:# If higher then floor_height it's Free
        mark = "F"
        if foot_height >= prev_foot_height and foot_height > next_foot_height:# If in highest position it's Free Up
            mark = "FU"
    else: # If equal or lower then floor_height it's Contact
        mark = "C"
        if frame == 1 or prev_foot_height > floor_height:# On start or previous was above floor height
            mark = "CS" 
        if frame == durration or next_foot_height > floor_height:# On end or next is above floor height
            mark = "CE"
    return mark    


# GET OFFSET PER FRAME
def get_OPF(frame, durration, fCurve_forward):
    foot_loc = fCurve_forward.evaluate(frame)
    prev_foot_loc = fCurve_forward.evaluate(frame-1)
    if frame == 1:
        prev_foot_loc = fCurve_forward.evaluate(durration)# Get last frame
    opf = prev_foot_loc - foot_loc # Opf is the difference of previous and current position
    return round(opf, 4)
   

class WLK_AnalizeWalkCycle(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.wlk_analyze_walk_cycle"
    bl_label = "Analize Walk Cycle"

    def execute(self, context):

        wlk_rig_action = WLK['wlk01']['source_action']

        # Break if walk cycle action not found
        if bpy.data.actions.find(wlk_rig_action) == -1:
            print("\nWLK Analize Walk Cycle / ERROR: Walk cycle action not found!")
            return {'FINISHED'}

        wlk_rig = WLK['wlk01']['rig_name']
        wlk_feet = WLK['wlk01']['bones_feet']

        WLK['wlk01']['walk_cycle_data'] = []# Clear previous data

        # Get fCurves
        feet_fCurves = {} # Collect foot animation fCurves from walk cycle
        for foot in wlk_feet:
            feet_fCurves[foot] = {}
            loc_data_path = 'pose.bones["'+foot+'"].location'
            feet_fCurves[foot]['loc_X'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, loc_data_path, 0) 
            feet_fCurves[foot]['loc_Y'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, loc_data_path, 1)
            feet_fCurves[foot]['loc_Z'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, loc_data_path, 2)                 
            rot_data_path = 'pose.bones["'+foot+'"].rotation_quaternion'
            feet_fCurves[foot]['rot_W'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, rot_data_path, 0)
            feet_fCurves[foot]['rot_X'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, rot_data_path, 1)
            feet_fCurves[foot]['rot_Y'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, rot_data_path, 2)
            feet_fCurves[foot]['rot_Z'] = get_fCurveByDPathAndArrayIndex(wlk_rig_action, rot_data_path, 3)

        duration = get_actionDuration(wlk_rig_action)
        f = 1
        while f <= duration:# Iterate each frame of walk cycle

            tmp_data = {}# Temporally holder (dict) for foot data

            for foot in wlk_feet:

                # Get current mark
                floor_height = WLK['wlk01']['bones_feet'][foot]['floor_height']
                mark = get_markAtFrame(f, duration, feet_fCurves[foot]['loc_Z'], floor_height)

                # Get OPF value, must detect foot mark first
                opf = 0
                if mark == "C" or mark == "CE":
                    opf = get_OPF(f, duration, feet_fCurves[foot]['loc_Y'])

                # Get transforms, must detect foot mark first
                transforms = None
                if mark == "CS" or mark == "FU":
                    fcs = feet_fCurves[foot]
                    loc = Vector (( fcs['loc_X'].evaluate(f),fcs['loc_Y'].evaluate(f),fcs['loc_Z'].evaluate(f) ))
                    rot = Quaternion (( fcs['rot_W'].evaluate(f), fcs['rot_X'].evaluate(f), fcs['rot_Y'].evaluate(f),fcs['rot_Z'].evaluate(f) ))
                    transforms = {"loc":loc, "rot":rot}
            
                # Populate temporally holder for current foot data
                tmp_data[foot]={"mark":mark, "opf":opf, "transforms":transforms}

            # Add foot data to walk cycle data
            WLK['wlk01']['walk_cycle_data'].append( dict(tmp_data) )
            tmp_data.clear()# Temporally holder dict must be forced clear, it keeps instancing

            f += 1

        print("\nWLK Analize Walk Cycle Data for: "+wlk_rig_action)
        PrintTable.print_table(WLK['wlk01']['walk_cycle_data'], ["CS","FU"])

        return {'FINISHED'}


def register():
    bpy.utils.register_class(WLK_AnalizeWalkCycle)
    

def unregister():
    bpy.utils.unregister_class(WLK_AnalizeWalkCycle)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()