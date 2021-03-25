import bpy

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

# GET ACTION DURATION
def get_actionDuration(action_name):
    action = bpy.data.actions[action_name]
    duration = action.frame_range[1]-action.frame_range[0]
    print("Get action duration", action_name, duration)
    return duration

# FIND FCURVE
def get_fCurveByDPathAndArrayIndex(action_name, dataPath, arrayIndex):
    found = None
    for fcurve in bpy.data.actions[action_name].fcurves:     
        if fcurve.data_path == dataPath and fcurve.array_index == arrayIndex:
            found = fcurve
    if found == None:
        print("Get foot fCurve by array index", "WARNING: FCurve not found!", action_name, dataPath, arrayIndex)
    else:
        print("Get foot fCurve by array index", action_name, dataPath, arrayIndex)
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
    print("Get foot mark at frame", frame, foot_height, mark)
    return mark    

# GET OFFSET PER FRAME
def get_footData_OPF(frame, durration, fCurve_forward):
    foot_loc = fCurve_forward.evaluate(frame)
    prev_foot_loc = fCurve_forward.evaluate(frame-1)
    if frame == 1:
        prev_foot_loc = fCurve_forward.evaluate(durration)# Get last frame
    opf = prev_foot_loc - foot_loc
    print("Get foot offset per frame (OPF)", frame, opf)
    return round(opf, 4)

def printTableRow(type, cols, data):

    if type == "th":

        output = "+"
        for col in cols:
            output += "="*col + "+"
        print(output)

        col_width = ""
        col_width = "{:^1}"
        for col in cols:
            col_width += "{:^"+str(col)+"}"
            col_width += "{:^1}"        
        col_data = []
        col_data.append("|")
        for cd in data:
            col_data.append(cd)
            col_data.append("|") 
        print(col_width.format(*col_data))

    if type == "tr":

        output = "+"
        for col in cols:
            output += "-"*col + "+"
        print(output)

        col_width = ""
        col_width = "{:^1}"
        for col in cols:
            col_width += "{:^"+str(col)+"}"
            col_width += "{:^1}"        
        col_data = []
        col_data.append("|")
        for cd in data:
            col_data.append(cd)
            col_data.append("|") 
        print(col_width.format(*col_data))


    

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):

        wlk_rig = WLK['wlk01']['rig_name']
        wlk_rig_action = WLK['wlk01']['source_action']
        wlk_feet = WLK['wlk01']['bones_feet']

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

            print (f)

            for foot in wlk_feet:

                print (foot)

                # Get current mark
                floor_height = WLK['wlk01']['bones_feet'][foot]['floor_height']
                mark = get_footData_markAtFrame(f, duration, feet_fCurves[foot]['loc_Z'], floor_height)

                opf = 0
                if mark == "C" or mark == "CE":
                    # Get OPF value
                    opf = get_footData_OPF(f, duration, feet_fCurves[foot]['loc_Y'])
            
                WLK['wlk01']['bones_feet'][foot]['frames_data'].append({"frame":f, "mark":mark, "opf":opf})

            f += 1



        

        print(" ")

        output_data = ["|"]
        output_cols = [1]
        output_data.append("FOOT FRAMES DATA OUTPUT")
        output_cols.append(53)
        output_data.append("|")
        output_cols.append(1)
        printTableRow("th", output_cols, output_data)

        output_data = ["|"]
        output_cols = [1]
        for foot in wlk_feet:
            output_data.append(foot)
            output_cols.append(25)
            output_data.append("|")
            output_cols.append(1)
        printTableRow("th", output_cols, output_data)

        
        output_data = ["|"]
        output_cols = [1]
        for foot in wlk_feet:
            output_data.append("Frame")
            output_cols.append(7)
            output_data.append("Mark")
            output_cols.append(6)
            output_data.append("OPF")
            output_cols.append(10)
            output_data.append("|")
            output_cols.append(1)
        printTableRow("th", output_cols, output_data)

        f = 0
        while f < duration:
            output_data = ["|"]
            output_cols = [1]
            for foot in wlk_feet:
                frames_data = WLK['wlk01']['bones_feet'][foot]['frames_data'][f]
                output_data.append(frames_data["frame"])
                output_cols.append(7)
                output_data.append(frames_data["mark"])
                output_cols.append(6)
                output_data.append(frames_data["opf"])
                output_cols.append(10)
                output_data.append("|")
                output_cols.append(1)
            printTableRow("tr", output_cols, output_data)
            f += 1
        
        print(" ")
         
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SimpleOperator)
    

def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()