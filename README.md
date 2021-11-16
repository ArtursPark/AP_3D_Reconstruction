Section 0 : Fun

    https://www.youtube.com/watch?v=GMil9tpwE_Q&ab_channel=PhotogrammetryBestPractices

Section 1 : Introduction

    The goal of this project is to be able to perform 3D reconstruction using a monocular structure from motion method. This project is to be continuously worked on.

Section 2 : Requirements

    Software :
    	Python 3.9

    Packages :
    	opencv==4.5.3.56
    	numpy==1.19.5
    	plotly==5.3.1

Section 3 : How-To Step by Step

    Step 0 : Clone the repo.
    	git clone ...

    Step 1 : Calibrate your camera.
    	i : Print the chessboard and tape it onto a hard surface.
    	ii : Take a few images of the chessboard from various angles.
    	iii : Run the calibration app to obtain a file containing intrinsic matrix and distortion coefficients.

    Step 2 : Perform 3D reconstruction.
    	i : Run the reconstruction against the input stream, plus calibration data obtained from the previous step.

Section 4 : App Documentations

    Commands :
    	1. [reconstruction] :
    		Arguments : Path, Stream, Calibration, Display Stream, Display Reconstruction.

    	2. [calibrate] :
    		Arguments : Path, Image File Type, Square Size, Rows, Columns, Output.

    	3. [video_to_images] :
    		Arguments : Path, Image Name, Image File Type, Output.

    Arguments :
    	1. Path [-p, --path] :
    		Description : Path to relevant file or directory.
    		Values : str
    		Default : "./data/input/sample*" , note : depends on the command.

    	2. Stream [-s, --stream] :
    		Description :
    			Chooses where the data will come from. If its a video or set of images, a path to file or directory, respectively, will need to be provided using path.
    		Values : "IMAGE", "VIDEO", "CAMERA".
    		Default : "CAMERA".

    	3. Image Name [-i, --image_name] :
    		Description :
    			Name of the image files. Example "my_cool_image_name.jpg", "my_cool_image_name" would be considered an image name.
    		Values : str
    		Default : ""

    	4. Image File Type [-t, --image_file_type] :
    		Description :
    			Name of the file extension on Windows. Example from Image Name argument, "jpg", would be considered an image file type.
    		Values : str
    		Default : "jpg"

    	5. Output [-o, --output] : Output file or directory.
    		Description :
    		Values : str
    		Default : "./data/output/output.txt" or "./data/output/"

    	6. Calibration [-c, --calibration] : Path to the calibration file.
    		Description :
    		Values : str
    		Default : "./calibration/data/output/output.txt"

    	7. Display Stream [-d, --display_stream] :
    		Description :
    		Values : "ON", "OFF".
    		Default : "OFF".

    	8. Display Reconstruction [-d, --display_reconstruction] :
    		Description :
    		Values : "ON", "OFF".
    		Default : "OFF".

    	9. Square Size [-s, --square_size] :
    		Description : Size of the square in the chessboard.
    		Values : float
    		Default : 0.0027

    	10. Rows [-r, --rows] :
    		Description : Number of rows in the chessboard.
    		Values : int
    		Default : 7

    	11. Columns [-c, --columns] :
    		Description : Number of columns in the chessboard.
    		Values : int
    		Default : 9

Section 5 : Computer Vision Topic Documentations

    I have posted my personal notes as pdf files, going over many relevant topics. This includes camera calibration, features, triangulation, etc. .

    git/documentation/my_notes/*.pdf

Section 6 : TODO Items

    This is a list of todo items to keep track of, as well as add anything I can think of, hence its a long list.

    git/documentation/TODO_List.txt

Section 7 : References

    This contains a list of my readings (opinions on them), and learning resources I have used and am currently using.

    git/documentation/references.txt

    Certain papers of interest are in "git/documentation/papers/*.pdf".

Section 8 : Contact Me

    Please, email me at arturspark1995@gmail.com.
    Thank you.
