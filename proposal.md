# Title
Terrain Visualizer

## Repository
https://github.com/Itsjustmeblank/Terrain-Visualizer.git

## Description
I want to create a program that can be run in maya to color a mesh based on height(or other conditions). This can be useful in sculpted or generated terrain to quickly color the mesh in regards to elevation.

## Features
- Feature 1
	- Run loop to determine the height(y-axis)
- Feature 2
	- Color based on height and/or additional modifiers(gradients?)
- Feature N 
	- Potentially add shading/noise or create variable color palletes based on inputed climate

## Challenges
- Familiarization of maya specific python system
- Effective ways to create terrain in maya
- Potentially arnold or other texturing software

## Outcomes
Ideal Outcome:
- A program that colors terrain, and can be modified by input to color based on specific terrain(hot,cold,wet,dry,land,sea) and certain parts of the terrain mesh can be modified(mountain to volcano, river to canyon) 

Minimal Viable Outcome:
- A limited texture that will color a preset mesh based on height. 0 y-axis is green, -10 is blue or brown, +25 is white mountain tops

## Milestones

- Week 1
  1. Familiarize with neccesary software
  2. Set up loop

- Week 2
  1. Troubleshoot
  2. Adjust coloring(gradient & potential texturing)

- Week N (Final)
  1. Allow for variation on input "Is this climate hot, mild, or cold?"
  2. Allow for modification of mesh to be recieved and then modify the coloring(Vertices/lines/faces that are *** wil be changed from this white to red or brown to blue)