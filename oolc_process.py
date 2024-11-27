import os
import glob
import copy
import yaml
import shutil
import oom_corel
import oom_git
import oom_base
import oom_markdown
import sys

def main(**kwargs):
    base_directory = kwargs.get('directory', os.getcwd())
    kwargs["base_directory"] = base_directory
    #find recursively all directories named oolc_production
    directories = glob.glob(f"{base_directory}/**/oolc_production", recursive=True)
    kwargs["oolc_directories"] = directories
    process_oolc_directories(**kwargs)
    #find recursively all directories named scad_production
    directories = glob.glob(f"{base_directory}/**/scad_output", recursive=True)
    kwargs["scad_directories"] = directories
    process_scad_directories(**kwargs)
    
    
    kwargs["comment"] = "comitting after processing for oolc"
    #oom_base.image_resolutions_dir(directory=base_directory, overwrite=True)
    #oom_git.push_to_git(**kwargs)

    

def process_oolc_directories(**kwargs):
    for directory in kwargs["oolc_directories"]:
        p3 = copy.deepcopy(kwargs)
        p3["oolc_directory"] = directory
        process_oolc_directory(**p3)

def process_oolc_directory(**kwargs):
    directory = kwargs["oolc_directory"]
    #load directory/working.yaml
    deets = {}
    with open(f"{directory}/working.yaml", 'r') as stream:
        try:
            deets = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    kwargs.update(deets)
    default_values = []
    default_values.append(["material", "mdf"])
    default_values.append(["thickness", "3_mm"])
    for default_value in default_values:
        if default_value[0] not in kwargs:
            kwargs[default_value[0]] = default_value[1]
    
    
    if "production_format" in deets:
        production_formats = deets["production_format"]
        for format in production_formats:
            width = "0_mm"
            height = "0_mm"
            if format.startswith("a4"):
                width = "210_mm"
                height = "297_mm"
            elif format.startswith("1200_mm_900_mm"):
                width = "1200_mm"
                height = "900_mm"
            if "width" not in kwargs:
                production_formats[format]["width"] = width
            if "height" not in kwargs:
                production_formats[format]["height"] = height
            p3 = copy.deepcopy(kwargs)
            p3["format"] = format
            p3["format_details"] = production_formats[format]
            process_format(**p3)
  
    print(f"making readme")
    p3 = copy.deepcopy(kwargs)    
    dir_template = "C:/GH/oomlout_oolc_oopen_laser_cutting_production_format/templates"
    template_file = f"{dir_template}/oolc_production_readme_template.md.j2"
    p3["template_file"] = template_file
    p3["dict_data"] = kwargs
    cwd = os.getcwd()
    directory = f"{cwd}/oolc_production"
    p3["directory"] = directory
    oom_markdown.generate_readme_generic(**p3)

def process_scad_directories(**kwargs):
    for directory in kwargs["scad_directories"]:
        p3 = copy.deepcopy(kwargs)
        p3["scad_directory"] = directory
        process_scad_directory(**p3)

def process_scad_directory(**kwargs):
    directory = kwargs["scad_directory"]
    directory_base = directory
    #load directory/working.yaml
    deets = {}
    #get a list of directories
    directories = glob.glob(f"{directory}/*")
    
    #create a working.yaml like the oolc typed one
    working_deets = {}
    cwd = os.getcwd()
    cwd = cwd.replace("\\", "/")
    project_id = cwd.split("/")[-1]
    working_deets["project_id"] = project_id
    working_deets["project_name"] = project_id.replace("_", " ").capitalize()
    project_repo = f"https://github.com/oomlout/{project_id}"
    working_deets["project_repo"] = project_repo
    

    
    scad_parts = {}
    scad_parts["parts"] = {}
    for directory in directories:
        working_file_name = f"{directory}/working.yaml"
        if os.path.exists(working_file_name):
            with open(working_file_name, 'r') as stream:
                try:
                    deets = yaml.load(stream, Loader=yaml.FullLoader)
                    directory = directory.replace("\\", "/")
                    top_directory = directory.split("/")[-1]
                    scad_parts["parts"][top_directory] = deets
                except yaml.YAMLError as exc:
                    print(exc)
    working_deets.update(scad_parts)            
    #save as working.yaml
    with open(f"{directory_base}/working.yaml", 'w') as file:
        
        yaml.dump(working_deets, file)
    
    
    
    kwargs.update(scad_parts)
    default_values = []
    default_values.append(["material", "pla"])
    for default_value in default_values:
        if default_value[0] not in kwargs:
            kwargs[default_value[0]] = default_value[1]
    



    print(f"making readme")
    p3 = copy.deepcopy(kwargs)    
    dir_template = "C:/GH/oomlout_oolc_oopen_laser_cutting_production_format/templates"
    template_file = f"{dir_template}/scad_output_readme_template.md.j2"
    p3["template_file"] = template_file
    p3["dict_data"] = kwargs
    cwd = os.getcwd()
    directory = f"{cwd}/scad_output"
    p3["directory"] = directory
    oom_markdown.generate_readme_generic(**p3)


def process_format(**kwargs):
    directory = kwargs["oolc_directory"]
    base_directory = kwargs["base_directory"]
    format_details = kwargs["format_details"]
    file_input = format_details["file_location"]
    file_input_type = file_input.split(".")[-1]    
    format = kwargs["format"]
    overwrite = kwargs.get("overwrite", True)

    directory_output = f"{directory}/{format}"

    if not os.path.exists(directory_output):
        os.makedirs(directory_output)

    file_src = f"{base_directory}/{file_input}"
    file_dst = f"{directory_output}/working.{file_input_type}"
    # copy file
    shutil.copyfile(file_src, file_dst)

    filename = file_dst
    #if filename is a dxf
    if filename.endswith(".dxf"):
        oom_corel.dxf_to_cdr(filename=filename)
        filename = filename.replace(".dxf", ".cdr")
    elif filename.endswith(".svg"):
        print(f"converting to cdr currently skipped")
        filename_test = filename.replace(".svg", ".cdr")
        if not os.path.exists(filename_test):
            oom_corel.svg_to_cdr(filename=filename)        
        filename = filename.replace(".svg", ".cdr")
    #if filename ends in cdr
    if filename.endswith(".cdr"):
        oom_corel.generate_outputs(filename=filename, overwrite=overwrite)
        oom_base.image_resolutions_dir(directory=directory_output, overwrite=overwrite)
    









if __name__ == "__main__":
    kwargs = {}
    #see if -overwrite is in the arguments
    overwrite = False
    if "-overwrite" in sys.argv:
        overwrite = True
    kwargs["overwrite"] = overwrite
    #directory = "C:/GH/oomlout_oolc_oopen_laser_cutting_production_format/tmp/data/glassgarden_oolc_decorative_item_christmas_bauble"
    
    #kwargs["directory"] = directory
    main(**kwargs)