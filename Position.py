import bpy

frameRange = int(bpy.data.actions['CubeDance'].frame_range[1])

keyframe01_frame = int(bpy.data.actions['CubeDance'].fcurves[2].keyframe_points[0].co[0])
keyframe01_value = bpy.data.actions['CubeDance'].fcurves[2].keyframe_points[0].co[1]

keyframe02_frame = int(bpy.data.actions['CubeDance'].fcurves[2].keyframe_points[1].co[0])
keyframe02_value = bpy.data.actions['CubeDance'].fcurves[2].keyframe_points[1].co[1]

keyframe03_frame = int(bpy.data.actions['CubeDance'].fcurves[2].keyframe_points[2].co[0])
keyframe03_value = bpy.data.actions['CubeDance'].fcurves[2].keyframe_points[2].co[1]

curveLenght = bpy.data.objects['BezierCurve'].data.splines.active.calc_length()

#bpy.data.actions['CubeDance'].fcurves[2].data_path
#bpy.data.actions['CubeDance'].fcurves[2].array_index

print("Frame Range="+str(frameRange))

print("First Keyframe at "+str(keyframe01_frame)+" frame, with value "+str(keyframe01_value))
print("Second Keyframe at "+str(keyframe02_frame)+" frame, with value "+str(keyframe02_value))
print("Third Keyframe at "+str(keyframe03_frame)+" frame, with value "+str(keyframe03_value))

print("And Lenght of Your curve is "+str(curveLenght))