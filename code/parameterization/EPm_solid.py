# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2021 replay file
# Internal Version: 2020_03_06-22.50.37 167380
# Run by ROG on Sun Oct 27 20:48:30 2024
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=85.328125, 
    height=140.111114501953)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
# 创建Part
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(36.25, 15.0))
s.ObliqueDimension(vertex1=v[3], vertex2=v[0], textPoint=(8.05610656738281, 
    -5.6560001373291), value=4000.0)
s.ObliqueDimension(vertex1=v[2], vertex2=v[3], textPoint=(42.5183258056641, 
    9.01599884033203), value=1000.0)
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s, depth=100.0)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
e = p.edges
p.DatumPointByOffset(point=p.InterestingPoint(edge=e[0], rule=MIDDLE), vector=(
    0.0, 10.0, 0.0))
e1 = p.edges
p.DatumPointByOffset(point=p.InterestingPoint(edge=e1[0], rule=MIDDLE), 
    vector=(0.0, -10.0, 0.0))
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
e, v1, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d1[2], normal=e[0], cells=pickedCells)
pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
e1, v2, d2 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d2[3], normal=e1[15], 
    cells=pickedCells)
# 创建Material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((30000.0, 0.2), ))
# 创建Section
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
    material='Material-1', thickness=None)
# 赋予Section    
cells = c.getSequenceFromMask(mask=('[#7 ]', ), )
region = p.Set(cells=cells, name='Set-1')
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
# 赋予Orientation    
region = p.sets['Set-1']
orientation=None
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(region=region, 
    orientationType=GLOBAL, axis=AXIS_1, additionalRotationType=ROTATION_NONE, 
    localCsys=None, fieldName='', stackDirection=STACK_3)
# 进入Assembly模块
a = mdb.models['Model-1'].rootAssembly
# 导入Part
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name='Part-1-1', part=p, dependent=OFF)
# 创建Step 
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', nlgeom=ON)
# 创建FieldOutput
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'MISES', 'E', 'U', 'RF'))
# 创建Load
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#800 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='Surf-1')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=4.0, 
    amplitude=UNSET)
# 创建BC-1
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#400 ]', ), )
region = a.Set(faces=faces1, name='Set-1')
mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Initial', 
    region=region, u1=0.0, u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
# 创建BC-2 
faces1 = f1.getSequenceFromMask(mask=('[#8 ]', ), )
region = a.Set(faces=faces1, name='Set-2')
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Initial', 
    region=region, u1=UNSET, u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
# 布设Seed  
partInstances =(a.instances['Part-1-1'], )
a.seedPartInstance(regions=partInstances, size=20.0, deviationFactor=0.1, 
    minSizeFactor=0.1)
# 划分网格 
partInstances =(a.instances['Part-1-1'], )
a.generateMesh(regions=partInstances)
# 创建Job
mdb.Job(name='Job-b100', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)
# 提交Job
# mdb.jobs['Job-b100'].submit(consistencyChecking=OFF)











