# CeNTREX-motorized-linear-stage
 Code for controlling a motorized linear stage.
 The linear stage has 50mm effective travel driven by a NEMA 11 stepper motor controlled by an Arduino Uno with a CNC shield expansion board. The expansion board requires at least 12V 1A.
 | component | model |
 | ---| --- |
 | linear stage | Befenybay 50mm effective travel length linear stage actuator |
 | cnc shield | Kuman CNC Shield Expansion Board V3.0 |
 | arduino | Uno |
 | motor driver | A4988 |

## Mechanical
To mount the linear stage to an optical table (with 1" grid spacing between 1/4-20 tapped holes) an adapter was designed. The linear stage mounts to the adapter with 4-40 screws, and the adapter subsequently mounts to the optical table with 1/4-20 screws. See `/mechanical/Table Mount Linear Stage.SLDPRT`.   

To mount optics to the linear stage another adapter piece was designed. It mounts to the linear stage with m3 screws, and uses #8 screws to attach an optical post. See `/mechanical/Optics Mount Linear stage.SLDPRT`.
## Serial commands
The serial commands are written as `e1`, `m10000` etc. Each return is followed by a newline character `\n`
| command | parameter | description |
| --- | --- | --- |
| e | 0/1 | disable or enable motor |
| x | n/a | get current position |
| z | n/a | set current position to zero |
| m | int | move to position specified |
| q | n/a | stop moving, returns the current position on a line followed by `Not moving\n`
| s | int | set the delay in us between pulses send to the stepper motor |
| ? | n/a | get the identity of the attached unit

## Python Interface
```Python
stage = MotorizedLinearStage("COM5")

print(stage.identity) # get the identity of the attached unit 

stage.position # get the current position in motor steps
stage.move(10000) # move to position 10000, which corresponds to 50 mm displacement
stage.move(0) # move back to the original position
print(stage.position)
```

## Images
### Linear Stage
![Linear Stage](linear_stage_picture.jpg)
![Linear Stage Schematic](linear_stage_schematic.jpg)

### CNC shield
![CNC Shield](cnc_shield_picture.jpg)