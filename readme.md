# oomlout_oolc_oopen_laser_cutting_production_format
A file structure, color code, and set of utility functions to make producing laser cutting files easy to have manufactured.
## file structure  
### source files  
Everything goes in a directory called oolc_production
* oolc_production
  * working.yaml
    * project_id
    * project_name
    * project_repo
    * production_format
      * name based on size (a4, 1200_mm_900_mm, tileable)
        * required file_location (referenced from the repo base) (normally .cdr is native, if another format is used it must be importable into corel draw x4)
        * optional width
        * option height
### generated files
The files that are generated
* oolc_production
  * (production_file_id)_a4
    *   
## sizes
These are the sizes that are supported.
### a4
The design placed within an a4 sheet. If the design doesn't fit on a single sheet multiples can be defined _# to do extra ones. If it fits multiple times add this detail in the configuration yaml file.
* width: 210 mm
* height: 297 mm
### 1200_mm_900_mm  
The design placed in a 1200 mm x 900 mm sheet. If the design doesn't fit on a single sheet multiples can be defined _# to do extra ones. If it fits multiple times add this detail in the configuration yaml file.
* width: 1200 mm
* height: 900 mm
### tileable
A single version of the design put into an arbitrary sized sheet.
* width: variable
* height: variable
## cut styles 
### traditional cuts
| Cut Type 	| Colour 	| RGB 			| Code		| Cut Order		| Description 				  
| ----		| ----		| ----			| ----		| ----			| ----  
| Cut		| Black		| (0,0,0)		| CUTT-01	| 03			| Simple cut all the way through the material.  
| Etch		| Blue		| (0,0,255)		| ETCH-01	| 02			| Vector etch. (Like a line drawing)  
| Engrave	| Magenta	| (255,0,255) 	| ENGR-01	| 01			| Raster engrave. (Scans the image line by line)  
| No Cut	| Cyan		| (0,255,255) 	| NOCU-01	| 04			| Used for guidelines etc, anything you want in the drawing but don't want the laser to cut.
  
### special cuts
| Cut Type 		| Colour 	| RGB 			| Code		|	Cut Order	|	Description 				 
| ----			| ----		| ----			| ----		| ----			| ----  
| Dashed Cut	| Green		| (0,255,0)		| DASH-01	| 04			| Cuts a dashed line. This means the parts remain in a sheet and can be popped out. Cut and gap distances vary by material.  
| Cut Last		| Red		| (255,0,0)		| LAST-01	| 05			| When not cutting fully closed objects. Use this style to cut last (ie. leave a bounding box until last, or a part that falls out and fouls others)  
| Heavy Engrave	| Pink		| (255,153,204)	| ENGH-01	| 06			| A very deep engrave.
| Start Dashed	| Brown		| (102,51,51)	| STDA-01	| 07			| Start with a space, this can be used to make sure small pieces don't fall through.
| Dashed Etch	| Powder Blue	| (204,204,255)	| DASE-01	| 08		| Dashed engrave (adjustable time to time)
### materials
# mdf_3_mm_thickness
MDF that is three mm thick.
