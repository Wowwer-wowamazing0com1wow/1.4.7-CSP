import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            

def insert_logo(original_image, logo, percent_of_side=0):
    """ Rounds the corner of a PIL.Image
    
    original_image must be a PIL.Image
    Returns a new PIL.Image with rounded corners, where
    0 < percent_of_side < 1
    is the corner radius as a portion of the shorter dimension of original_image
    """
    #set the radius of the rounded corners
    width, height = original_image.size
    SideW = int(percent_of_side * width) # radius in pixels
    SideH = int(percent_of_side * height)
    ###
    #create a mask
    ###
    
    #start with transparent mask
    rounded_mask = PIL.Image.new('RGBA', (width, height), (255,0,0,0))
    drawing_layer = PIL.ImageDraw.Draw(rounded_mask)

    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    
    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.polygon([(SideW,SideH),(width-SideW,SideH),
                            (width-SideW,height-SideH),(SideW,height-SideH)],
                            fill=(127,0,127,255))

                         
    # Uncomment the following line to show the mask
    #plt.imshow(rounded_mask)
    
    
    # Make the new image, starting with all transparent
    #result = PIL.Image.new('RGBA', original_image.size, (100,0,0,100))
    '''logo = logo.convert('RGBA')
    print(type(original_image.size))
    
    
    result = PIL.Image.new('RGBA', original_image.size)
    print(type(result))
    result = PIL.Image.alpha_composite(result, original_image)
    print(type(result))
    result = PIL.Image.alpha_composite(result, logo)'''
    
    #result = PIL.Image.alpha_composite(original_image, logo)
    #result.paste(original_image, (0,0), mask=rounded_mask)
    #result.paste(logo, (0,0), mask=original_image)
    #plt.imshow(result)
    
    original_image = original_image.convert('RGBA')
    logo = logo.convert('RGBA')
    
    original_image.paste(logo, (0, 0), logo.convert('RGBA'))
    
    return original_image
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list
    
def get_logo(directory=None, type='black'):
    if directory == None:
        directory = os.getcwd()

    # gets file name for selected logo type
    if type == 'black':
        entry = 'logo 1 black.png'
    else:
        entry = 'logo 1 white.png'
        #entry == "CIRCLE PROJECT WaterMark.png"

    image = PIL.Image.open(directory + '/logos/' + entry)
    '''
    directory_list = os.listdir(directory)
    for entry in directory_list:
        if entry == "CIRCLE PROJECT WaterMark.png":
            absolute_filename = os.path.join(directory, entry)
            image = PIL.Image.open(absolute_filename)'''

    image = image.resize((300,60))
    return image

def insert_logo_all_images(directory=None):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    # Load all the images
    image_list, file_list = get_images(directory)  
    logo = get_logo()

    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        print(n)
        filename, filetype = os.path.splitext(file_list[n])
        
        # insert logo in image
        curr_image = image_list[n]
        new_image = insert_logo(curr_image, logo) 
        
        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    