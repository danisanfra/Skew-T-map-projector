isValid = False

folders_setup_path = './path_variables.py'
f = open(folders_setup_path,'r')
content = f.readlines()
f.close()

while not isValid:
    print()
    f = open(folders_setup_path, 'w')
    maps_path = str(input('Insert your \'/maps\' folder\'s path:\t'))
    
    content[0] = content[0][:15] + maps_path + '/maps/\'\n'
    
    for line in content:
        f.write(line)
    
    f.close()

    try:
        folders_setup_path = maps_path + '/maps/path_variables.py'
        f = open(folders_setup_path, 'r')
    except:
        print('Invalid path')
        f.close()
    else:
        isValid = True
        f.close()