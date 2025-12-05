import maya.cmds as cmds
import maya.api.OpenMaya as om

print("hi")
class TerrainVisualizer:

    def __init__(self, climate="mild"):         #default of mild
        self.climate = climate
        self.color_set_name = "terrainColorSet"
        self.mesh_dag = None
        self.mesh_fn = None


    def load_mesh(self):
        sel = om.MGlobal.getActiveSelectionList()
        print(f"[LOAD MESH] Selection count: {sel.length()}")

        if sel.length() == 0:                       #safegaurd 
            om.MGlobal.displayError("Please select a mesh.")
            return False

        dag = sel.getDagPath(0)             
        dag.extendToShape()
        print(f"[LOAD MESH] Mesh DAG path: {dag.fullPathName()}")

        self.mesh_dag = dag
        self.mesh_fn = om.MFnMesh(dag)
        print(f"[LOAD MESH] MFnMesh created for: {dag.fullPathName()}")

        return True

    def get_palette(self):           #actual RGBs
        palettes = {
            "hot":  [(0, (0.3, 0.1, 0.0)), (0.5, (1.0, 0.4, 0.0)), (1.0, (1.0, 1.0, 0.7))], #brown, red, yellow/tan
            "mild": [(0, (0.0, 0.3, 0.0)), (0.5, (0.2, 0.8, 0.2)), (1.0, (0.9, 0.9, 0.9))],
            "cold": [(0, (0.0, 0.0, 0.4)), (0.4, (0.5, 0.8, 1.0)), (1.0, (1.0, 1.0, 1.0))]
        }

        return palettes.get(self.climate, palettes["mild"])     #must run only mild, hot, or cold


    def lerp_color(self, c1, c2, t):                            #create gradient
        """lerp = c1 + (c2 - c1) * t"""
        return om.MColor([
            c1[0] + (c2[0] - c1[0]) * t,
            c1[1] + (c2[1] - c1[1]) * t,
            c1[2] + (c2[2] - c1[2]) * t,
            1.0
        ])

    def height_to_color(self, norm_height):             #height of verts to color
        palette = self.get_palette()                    #retrieve variables

        for i in range(len(palette) - 1):               #for loop based on height
            h1, c1 = palette[i]
            h2, c2 = palette[i + 1]

            if h1 <= norm_height <= h2:
                t = (norm_height - h1) / (h2 - h1)
                return self.lerp_color(c1, c2, t)


        last_color = palette[-1][1]

        """return [last_color[0], last_color[1], last_color[2], 1]"""      #if too high will just color with last rgb in the class
        return om.MColor((last_color[0], last_color[1], last_color[2], 1.0))
    def apply(self):
        if not self.load_mesh():
            return

        mesh = self.mesh_fn
        verts = mesh.getPoints(om.MSpace.kWorld)

    
        heights = [v.y for v in verts]
        min_h = min(heights)
        max_h = max(heights)
        height_range = max_h - min_h + 1e-6  # Prevent division by zero

        
        colors = [self.height_to_color((v.y - min_h) / height_range) for v in verts]


        if self.color_set_name not in mesh.getColorSetNames():           #create colorset
            mesh.createColorSet(self.color_set_name)

        mesh.setCurrentColorSetName(self.color_set_name)

        mesh.setColors(colors, self.color_set_name)


        
        
        mesh.setColors(colors, self.color_set_name)  # colors must match vertex count
        vertex_indices = list(range(len(colors)))
        mesh.assignColors(vertex_indices, colorSetName=self.color_set_name)



        mesh.updateSurface()

#mesh.assignColors(vertex_colors, self.color_set_name) #(list(range(len(colors))), self.color_set_name)"""

        mesh_name = self.mesh_dag.fullPathName()                     #lambert?
        shader = cmds.shadingNode("lambert", asShader=True, name="terrainShader")
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="terrainSG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader")
        cmds.sets(mesh_name, e=True, forceElement=sg)

        om.MGlobal.displayInfo(f"TerrainVisualizer: Coloring applied using '{self.climate}' climate.")


"""
import sys
import importlib

module_folder = r"C:\Users\jaker\OneDrive\Desktop\Programming\PFDA\Terrain_Visualizer\Terrain-Visualizer"
if module_folder not in sys.path:
    sys.path.append(module_folder)


import terrain_visualizer
importlib.reload(terrain_visualizer)

tv = terrain_visualizer.TerrainVisualizer(climate="mild")
tv.apply()
"""