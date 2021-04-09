import bpy
import math
from mathutils import Vector, Quaternion

wlk_collection = 'Novi Test'

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


def main(context):
    print("")
    print("")
    print("################################## WLK: INIT")
    print("")
    print("")

# MAKE NEW COLLECTION
def new_collection(name):
    
    collection = bpy.data.collections.get( name )
    if collection == None:
        collection = bpy.data.collections.new( name )
        
    if bpy.context.scene.collection.children.get( collection.name ) == None:
        bpy.context.scene.collection.children.link( collection )
        
    print('Create new collection', name)
   
    return collection

# MAKE NEW ARMATURE
def new_armature(name, collection):
    
    armature = bpy.data.armatures.get( name )
    if armature == None:
        armature = bpy.data.armatures.new( name )
    
    obj = bpy.data.objects.get( name )
    if obj == None:
        obj = bpy.data.objects.new( name, armature )
        
    if bpy.data.collections[collection].objects.get( obj.name ) == None:
        bpy.data.collections[collection].objects.link( obj )
        
    print('Create new armature', name)    
    return obj


# MAKE NEW ACTION
def new_action(name, obj):
    
    action = bpy.data.actions.get( name )
    if action == None:
        action = bpy.data.actions.new( name ) 
        
    if obj.animation_data == None:
        obj.animation_data_create()
    obj.animation_data.action = action
    
    print('Create new action', name)
    return action

# GET ACTION DURATION
def get_actionDuration(action_name):
    action = bpy.data.actions[action_name]
    duration = action.frame_range[1]-action.frame_range[0]
    print("Get action duration", action_name, duration)
    return duration

# GENERATE ANIMATION FROM WALK CYCLE AND REPEAT COUNT
def copyWalkCycleAndRepeat(source_action_name, source_action_repeat, wlk_action):
    
    source_duration = get_actionDuration(source_action_name)
    
    # Remove all frames    
    wlk_action_fcurves = wlk_action.fcurves
    for fcurve in wlk_action_fcurves:
        wlk_action_fcurves.remove(fcurve)
        
    # Copy fcurves from walk cycle
    souce_action = bpy.data.actions[source_action_name]
    for source_fcurve in souce_action.fcurves:
        # Make new fcurve in wlk_action
        wlk_action_fcurve = wlk_action_fcurves.new(data_path = source_fcurve.data_path, index = source_fcurve.array_index, action_group = source_fcurve.group.name)
        # Iterate keyframes and copy to new fcurve
        for source_keyframe in source_fcurve.keyframe_points:
            wlk_action_keyframe = wlk_action_fcurve.keyframe_points.insert(source_keyframe.co[0], source_keyframe.co[1])
            wlk_action_keyframe.handle_left_type = source_keyframe.handle_left_type
            wlk_action_keyframe.handle_right_type = source_keyframe.handle_right_type
            wlk_action_keyframe.interpolation = source_keyframe.interpolation
            wlk_action_keyframe.type = source_keyframe.type
            wlk_action_keyframe.easing = source_keyframe.easing
            wlk_action_keyframe.back = source_keyframe.back
            wlk_action_keyframe.amplitude = source_keyframe.amplitude
            wlk_action_keyframe.period = source_keyframe.period
            wlk_action_keyframe.handle_left = source_keyframe.handle_left
            wlk_action_keyframe.handle_right = source_keyframe.handle_right
        # Repeat walk cycle in WLK ACTION from first cycle
        offsetFrames = source_duration
        finalDuration = source_duration * source_action_repeat
        while offsetFrames < finalDuration:     
            for wlk_action_fcurve in wlk_action_fcurves:        
                for wlk_action_keyframe in wlk_action_fcurve.keyframe_points:
                    if wlk_action_keyframe.co[0] <= source_duration+1:# Duplicate only from first cycle with last frame
                        if wlk_action_keyframe.co[0] == 1:# Skip first frame, leave last, just fix right handles from first
                            last_keyframe = wlk_action_fcurve.keyframe_points[-1]
                            last_keyframe.handle_right_type = 'FREE'
                            last_keyframe.handle_right = [wlk_action_keyframe.handle_right[0]+offsetFrames,wlk_action_keyframe.handle_right[1]]
                        else:
                            new_keyframe = wlk_action_fcurve.keyframe_points.insert(wlk_action_keyframe.co[0]+offsetFrames, wlk_action_keyframe.co[1])
                            new_keyframe.handle_left_type = wlk_action_keyframe.handle_left_type
                            new_keyframe.handle_right_type = wlk_action_keyframe.handle_right_type
                            new_keyframe.interpolation = wlk_action_keyframe.interpolation
                            new_keyframe.type = wlk_action_keyframe.type
                            new_keyframe.easing = wlk_action_keyframe.easing
                            new_keyframe.back = wlk_action_keyframe.back
                            new_keyframe.amplitude = wlk_action_keyframe.amplitude
                            new_keyframe.period = wlk_action_keyframe.period
                            new_keyframe.handle_left = [wlk_action_keyframe.handle_left[0]+offsetFrames,wlk_action_keyframe.handle_left[1]]
                            new_keyframe.handle_right = [wlk_action_keyframe.handle_right[0]+offsetFrames,wlk_action_keyframe.handle_right[1]]
            offsetFrames += source_duration
    print ("Copy animation from walk cycle", source_action_name)


# MOVE BONE IN POSE MODE, NO KEYFRAMES ADDED
def move_bone(rig_name, bone_name, loc, rot):
    
    rig_obj = bpy.data.objects.get(rig_name)
    bpy.context.view_layer.objects.active = rig_obj
    rig_obj.select_set(True)
    bpy.ops.object.mode_set(mode='POSE') 
    bone = rig_obj.pose.bones[bone_name]
    bone.location = loc
    bone.rotation_quaternion = rot
    bpy.ops.object.mode_set(mode='OBJECT') 
    
    print('Move bone', rig_name, bone_name)


# ADD COPY TRANSFORMS TO BONE
def const_copyTransf(rig_name, bone_name, target_rig_name, target_bone_name):
    
    # Make constraint to root
    bone = bpy.data.objects[rig_name].pose.bones[bone_name]
    bone_const_name = "WLK_COPY_TRANS"
    bone_const = bone.constraints[bone_const_name]
    if bone_const == None:
        bone_const = bone.constraints.new('COPY_TRANSFORMS')
        bone_const.name = bone_const_name
    bone_const.target = bpy.data.objects[target_rig_name]
    bone_const.subtarget = target_bone_name
    
    print('Constraint Copy Transform', rig_name, bone_name, target_rig_name, target_bone_name)


# EDIT EXISTING BONE
def edit_bone(rig_name, bone_name, head, tail, matrix):
    
    armature = bpy.data.armatures.get(rig_name)  
        
    rig_obj = bpy.data.objects.get(rig_name)
    bpy.context.view_layer.objects.active = rig_obj
    rig_obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')    
    
    bone = armature.edit_bones.get(bone_name)
    bone.head = head
    bone.tail = tail
    if matrix != None:
        bone.matrix = matrix
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print('Edit bone', rig_name, bone_name, head, tail, matrix)


# DUPLICATE BONES BETWEEN RIGS
def copy_bone(source_rig_name, source_bone_name, target_rig_name, target_bone_name, parent_bone):
    
    source_armature = bpy.data.armatures.get(source_rig_name)
    target_armature = bpy.data.armatures.get(target_rig_name)    
    source_bone = source_armature.bones.get(source_bone_name)
        
    target_rig_obj = bpy.data.objects.get(target_rig_name)
    bpy.context.view_layer.objects.active = target_rig_obj
    target_rig_obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    
    
    target_bone = target_armature.edit_bones.get(target_bone_name)
    if target_bone == None:        
        target_bone = target_armature.edit_bones.new(target_bone_name)
    target_bone.head = source_bone.head_local
    target_bone.tail = source_bone.tail_local
    target_bone.matrix = source_bone.matrix_local
    if parent_bone != None:
        target_bone.parent = target_armature.edit_bones.get(parent_bone)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print('Copy bone', source_rig_name, target_rig_name, target_bone_name)
    return target_armature.bones.get(target_bone_name)


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


# FIND MARK AT FRAME
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


def get_footData_OPF(frame, durration, fCurve_forward):
    foot_loc = fCurve_forward.evaluate(frame)
    prev_foot_loc = fCurve_forward.evaluate(frame-1)
    if frame == 1:
        prev_foot_loc = fCurve_forward.evaluate(durration)# Get last frame
    opf = prev_foot_loc - foot_loc
    print("Get foot offset per frame (OPF)", frame, opf)
    return opf



def animate_followPath(rig_name, hlp_rig_name, hlp_bones_root_name, path_name, wlk_action_name, hlp_action_name, feet):
    
    followPath_value = 0 
    
    # Make follow path constraint
    hlp_root = bpy.data.objects[hlp_rig_name].pose.bones[hlp_bones_root_name]
    hlp_root_const_name = "WLK FOLLOW PATH"
    hlp_root_const = hlp_root.constraints.get(hlp_root_const_name)
    if hlp_root_const == None:
        hlp_root_const = hlp_root.constraints.new('FOLLOW_PATH')
        hlp_root_const.name = hlp_root_const_name
    hlp_root_const.target = bpy.data.objects[path_name]
    hlp_root_const.offset = followPath_value
    hlp_root_const.forward_axis = 'TRACK_NEGATIVE_Y'
    hlp_root_const.use_curve_follow = True
    
    # Make follow path fCurve
    followPath_dataPath = 'pose.bones["'+hlp_bones_root_name+'"].constraints["'+hlp_root_const_name+'"].offset'
    followPath_fCurve = get_fCurveByDPathAndArrayIndex(hlp_action_name, followPath_dataPath, 0)
    if followPath_fCurve == None:  
        followPath_fCurve = bpy.data.actions[hlp_action_name].fcurves.new(data_path = followPath_dataPath)
    
    feet_fCurves = {} # To search for specific feet fCurve just once and to keep it here
    jumper_fCurves = {} # To search for specific jumper fCurve just once and to keep it here
    path_len = bpy.data.objects[path_name].data.splines.active.calc_length() 
    duration = get_actionDuration(wlk_action_name)
    f = 1
    while f <= duration:
        root_OPFs = []# Use more then one OPF to support more then 2 legs
        CSs = []
        for foot in feet:# Check for all feet
            foot_name = foot
            floor_height = feet[foot]["floor_height"]
            if feet_fCurves.get(foot_name) == None:
                feet_fCurves[foot_name] = {}
                loc_data_path = 'pose.bones["'+foot_name+'"].location'
                feet_fCurves[foot_name]['loc_X'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, loc_data_path, 0)
                feet_fCurves[foot_name]['loc_Y'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, loc_data_path, 1)
                feet_fCurves[foot_name]['loc_Z'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, loc_data_path, 2)                
                rot_data_path = 'pose.bones["'+foot_name+'"].rotation_quaternion'
                feet_fCurves[foot_name]['rot_W'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, rot_data_path, 0)
                feet_fCurves[foot_name]['rot_X'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, rot_data_path, 1)
                feet_fCurves[foot_name]['rot_Y'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, rot_data_path, 2)
                feet_fCurves[foot_name]['rot_Z'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, rot_data_path, 3)
                jumper_inf_data_path = 'pose.bones["'+foot_name+'"].constraints["WLK_COPY_TRANS"].influence'
                feet_fCurves[foot_name]['inf'] = get_fCurveByDPathAndArrayIndex(wlk_action_name, jumper_inf_data_path, 0)
                # Add influence fCurves for feet
                
            # Get current mark
            mark = get_footData_markAtFrame(f, duration, feet_fCurves[foot_name]['loc_Z'], floor_height)
            # Add OPF only for Contact and Contact End
            if mark == "C" or mark == "CE":
                # Get OPF value
                root_OPFs.append(get_footData_OPF(f, duration, feet_fCurves[foot_name]['loc_Y']))
            if mark == "CS":
                
                #ANIMATE JUMPER INFLUENCE
                keyframe = feet_fCurves[foot_name]['inf'].keyframe_points.insert(f, 1)
                keyframe.interpolation = 'CONSTANT'
                
                loc = Vector (( feet_fCurves[foot_name]['loc_X'].evaluate(f),feet_fCurves[foot_name]['loc_Y'].evaluate(f),feet_fCurves[foot_name]['loc_Z'].evaluate(f) ))
                rot = Quaternion (( feet_fCurves[foot_name]['rot_W'].evaluate(f), feet_fCurves[foot_name]['rot_X'].evaluate(f), feet_fCurves[foot_name]['rot_Y'].evaluate(f),feet_fCurves[foot_name]['rot_Z'].evaluate(f) ))
                CSs.append({"foot_name":foot_name, "loc":loc, "rot":rot})
                
                if jumper_fCurves.get(foot_name) == None:
                    jumper_name = "JUMPER."+foot_name
                    fcurves = bpy.data.actions[hlp_action_name].fcurves
                    jumper_fCurves[foot_name] = {}
                    
                    jumper_loc_dataPath = 'pose.bones["'+jumper_name+'"].location'
                    if get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_loc_dataPath, 0) == None:
                        jumper_fCurves[foot_name]['loc_X'] = fcurves.new(data_path=jumper_loc_dataPath, index=0, action_group=jumper_name)
                        jumper_fCurves[foot_name]['loc_Y'] = fcurves.new(data_path=jumper_loc_dataPath, index=1, action_group=jumper_name)
                        jumper_fCurves[foot_name]['loc_Z'] = fcurves.new(data_path=jumper_loc_dataPath, index=2, action_group=jumper_name)                
                    else:
                        jumper_fCurves[foot_name]['loc_X'] = get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_loc_dataPath, 0)
                        jumper_fCurves[foot_name]['loc_Y'] = get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_loc_dataPath, 1)
                        jumper_fCurves[foot_name]['loc_Z'] = get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_loc_dataPath, 2) 
                    
                    jumper_rot_dataPath = 'pose.bones["'+jumper_name+'"].rotation_quaternion'
                    if get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_rot_dataPath, 0) == None:
                        jumper_fCurves[foot_name]['rot_W'] = fcurves.new(data_path=jumper_rot_dataPath, index=0, action_group=jumper_name)
                        jumper_fCurves[foot_name]['rot_X'] = fcurves.new(data_path=jumper_rot_dataPath, index=1, action_group=jumper_name)
                        jumper_fCurves[foot_name]['rot_Y'] = fcurves.new(data_path=jumper_rot_dataPath, index=2, action_group=jumper_name)
                        jumper_fCurves[foot_name]['rot_Z'] = fcurves.new(data_path=jumper_rot_dataPath, index=3, action_group=jumper_name)
                    else:
                        jumper_fCurves[foot_name]['rot_W'] = get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_rot_dataPath, 0)
                        jumper_fCurves[foot_name]['rot_X'] = get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_rot_dataPath, 1)
                        jumper_fCurves[foot_name]['rot_Y'] = get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_rot_dataPath, 2)
                        jumper_fCurves[foot_name]['rot_Z'] = get_fCurveByDPathAndArrayIndex(hlp_action_name, jumper_rot_dataPath, 3)
            if mark == "CE":          
                keyframe = feet_fCurves[foot_name]['inf'].keyframe_points.insert(f, 0)
                keyframe.interpolation = 'CONSTANT'
                

        # Use average value for OPF
        if len(root_OPFs) > 0:
            avr_root_OPF = 0
            for opf in root_OPFs:
                avr_root_OPF += opf
            avr_root_OPF = avr_root_OPF/len(root_OPFs)
            # Convert to followPath %
            followPath_value += avr_root_OPF/path_len*100
        followPath_fCurve.keyframe_points.insert(f, followPath_value)
        
        # Dirty fix to test feets and jumpers concept
        for foot in CSs:
            
            foot_name = foot["foot_name"]
            
            hlp_root_name = hlp_bones_root_name+".CS."+str(f)
            copy_bone(rig_name, hlp_bones_root_name, hlp_rig_name, hlp_root_name, None)
            
            
            hlp_foot_name = foot_name+".CS."+str(f)
            copy_bone(rig_name, foot_name, hlp_rig_name, hlp_foot_name, hlp_root_name)
            move_bone(hlp_rig_name, hlp_foot_name, foot["loc"], foot["rot"])
            
            
            # Make follow path constraint and animation fcurve
            hlp_root = bpy.data.objects[hlp_rig_name].pose.bones[hlp_root_name]
            hlp_root_const_name = "WLK FOLLOW PATH"
            hlp_root_const = hlp_root.constraints.get(hlp_root_const_name)
            if hlp_root_const == None:
                hlp_root_const = hlp_root.constraints.new('FOLLOW_PATH')
                hlp_root_const.name = hlp_root_const_name
            hlp_root_const.target = bpy.data.objects[path_name]
            hlp_root_const.offset = followPath_value
            hlp_root_const.forward_axis = 'TRACK_NEGATIVE_Y'
            hlp_root_const.use_curve_follow = True
            
            # MOVE JUMPERS
            jumper_new_loc = None;
            jumper_new_rot = None;
            hlp_rig_obj = bpy.data.objects.get(hlp_rig_name)
            bpy.context.view_layer.objects.active = hlp_rig_obj
            hlp_rig_obj.select_set(True)
            bpy.ops.object.mode_set(mode='POSE') 
            bone = hlp_rig_obj.pose.bones[hlp_foot_name]
            jumper_new_loc = bone.head
            jumper_new_rot = bone.matrix.to_quaternion()
            bpy.ops.object.mode_set(mode='OBJECT') 
            keyframe = jumper_fCurves[foot_name]['loc_X'].keyframe_points.insert(f, jumper_new_loc[0])
            keyframe.interpolation = 'CONSTANT'
            keyframe = jumper_fCurves[foot_name]['loc_Y'].keyframe_points.insert(f, jumper_new_loc[1])
            keyframe.interpolation = 'CONSTANT'
            keyframe = jumper_fCurves[foot_name]['loc_Z'].keyframe_points.insert(f, jumper_new_loc[2])
            keyframe.interpolation = 'CONSTANT'
            keyframe = jumper_fCurves[foot_name]['rot_W'].keyframe_points.insert(f, jumper_new_rot[0])
            keyframe.interpolation = 'CONSTANT'
            keyframe = jumper_fCurves[foot_name]['rot_X'].keyframe_points.insert(f, jumper_new_rot[1])
            keyframe.interpolation = 'CONSTANT'
            keyframe = jumper_fCurves[foot_name]['rot_Y'].keyframe_points.insert(f, jumper_new_rot[2])
            keyframe.interpolation = 'CONSTANT'
            keyframe = jumper_fCurves[foot_name]['rot_Z'].keyframe_points.insert(f, jumper_new_rot[3])
            keyframe.interpolation = 'CONSTANT'
            
            
        print("Animate FollowPath", f, root_OPFs, followPath_value)
        f += 1


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        # Example with single walker simulation
        walker_id = 'wlk01'
        # Create walker collection
        new_collection(wlk_collection)
        # Create helper armature and add helper action
        hlp_rig_obj = new_armature(WLK[walker_id]['hlp_rig'], wlk_collection)
        hlp_action = new_action(WLK[walker_id]['hlp_action'], hlp_rig_obj)
        
        # Create walker action to original rig
        rig_obj = bpy.data.objects.get(WLK[walker_id]['rig_name'])
        wlk_action = new_action(WLK[walker_id]['wlk_action'], rig_obj)

        # Generate animation in walker action from walk cycle repeated requested number of times
        #copyWalkCycleAndRepeat(WLK[walker_id]['source_action'], WLK[walker_id]['source_action_repeat'], wlk_action)

        # Make helper root bone and assing constraint to root bone in original rig to copy transforms
        copy_bone(WLK[walker_id]['rig_name'], WLK[walker_id]['bones_root'], WLK[walker_id]['hlp_rig'], WLK[walker_id]['bones_root'], None)
        const_copyTransf(WLK[walker_id]['rig_name'], WLK[walker_id]['bones_root'], WLK[walker_id]['hlp_rig'], WLK[walker_id]['bones_root'])

        # Prepare JUMPERS (feet in original rig having constraint to copy transforms from Jumpers)
        for foot in WLK[walker_id]['bones_feet']:
    
            # Add jumper helper for current foot
            foot_name = foot
            jumper_name = 'JUMPER.'+foot_name
            jumper = copy_bone(WLK[walker_id]['rig_name'], foot_name, WLK[walker_id]['hlp_rig'], jumper_name, None)
            edit_bone(WLK[walker_id]['hlp_rig'], jumper_name, Vector((0,0,0)), Vector((0,0.1,0)), None)
    
            # Add constraint to copy transforms from jumpers
            const_copyTransf(WLK[walker_id]['rig_name'], foot_name, WLK[walker_id]['hlp_rig'], jumper_name)
    
            # Add fCurves to rig foot to animate influece
            const_inf_dataPath = 'pose.bones["'+foot_name+'"].constraints["WLK_COPY_TRANS"].influence'
            if get_fCurveByDPathAndArrayIndex(WLK[walker_id]['wlk_action'], const_inf_dataPath, 0) == None:
                bpy.data.actions[WLK[walker_id]['wlk_action']].fcurves.new(data_path=const_inf_dataPath, index=0, action_group=foot_name)
                        

        # Generate animation
        animate_followPath(WLK[walker_id]['rig_name'], WLK[walker_id]['hlp_rig'], WLK[walker_id]['bones_root'], WLK[walker_id]['path'], WLK[walker_id]['wlk_action'], WLK[walker_id]['hlp_action'], WLK[walker_id]['bones_feet'])
        


        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)
    

def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()