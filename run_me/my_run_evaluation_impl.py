from typing import Optional, List
import nibabel as nib
import numpy as np
import numpy.typing as npt
import pyvista as pv

def compute_the_delaunay(COMPRESSED_NII_FILENAME:str, DATA: npt.NDArray[np.float64], my_data_labels_which_are_a_guess:list[str], my_colors, MY_DATA_THRESHOLD:float = 0.1e0)->None:
    plotter = pv.Plotter(off_screen=False, window_size=[1024, 1024])
    [plot_the_results(my_delaunay_calculation_result, [my_data_labels_which_are_a_guess, COMPRESSED_NII_FILENAME], index, my_colors, plotter) for index, my_delaunay_calculation_result in enumerate([pv.PolyData(nib.affines.apply_affine(nib.load(COMPRESSED_NII_FILENAME).affine, np.argwhere(DATA > MY_DATA_THRESHOLD))[mask]).delaunay_3d(alpha=1.0) for mask in [(DATA[tuple(np.argwhere(DATA > MY_DATA_THRESHOLD).T)] == index) for index in range(1, len(my_data_labels_which_are_a_guess)+1)]])]
    plotter.set_background(color='white')
    plotter.show_bounds()
    plotter.show()
    #plotter.screenshot('after_delaunay.png')
    return None

def plot_the_results(my_delaunay_results, list_containing_labels_and_filename, index, colors, plotter):
    pv.global_theme.allow_empty_mesh = True
    my_color = colors[index]
    labels = list_containing_labels_and_filename[0]
    filename = list_containing_labels_and_filename[1]
    plotter.add_mesh(my_delaunay_results, color=my_color, opacity=1.0, show_edges=True)
    return

def check_if_computing_the_delaunay_of_the_mesh_was_a_success(my_delaunay_results, list_containing_labels_and_filename, index, colors)->bool:
    pv.global_theme.allow_empty_mesh = True

    my_color = colors[index]
    labels = list_containing_labels_and_filename[0]
    filename = list_containing_labels_and_filename[1]

    try:
        plotter = pv.Plotter()
        plotter.add_mesh(my_delaunay_results, color=my_color, opacity=1.0, show_edges=True)
        plotter.add_text(f"filename[index]]: {filename[index]} labels[index]:{labels[index]}", font_size=14, position='upper_left')
        plotter.show()
    except Exception as ex:
        print(f"ex {ex}")
        return False
    return True

def the_delaunay_of_the_mesh_was_successful(COMPRESSED_NII_FILENAME:str, DATA: npt.NDArray[np.float64], my_data_labels_which_are_a_guess:list[str], my_colors, MY_DATA_THRESHOLD:float = 0.1e0)->list[bool]:
    return [check_if_computing_the_delaunay_of_the_mesh_was_a_success(my_delaunay_calculation_result, [my_data_labels_which_are_a_guess, COMPRESSED_NII_FILENAME], index, my_colors) for index, my_delaunay_calculation_result in enumerate([pv.PolyData(nib.affines.apply_affine(nib.load(COMPRESSED_NII_FILENAME).affine, np.argwhere(DATA > MY_DATA_THRESHOLD))[mask]).delaunay_3d(alpha=1.0) for mask in [(DATA[tuple(np.argwhere(DATA > MY_DATA_THRESHOLD).T)] == index) for index in range(1, len(my_data_labels_which_are_a_guess)+1)]])]

def plot_if_delaunay_was_a_success(COMPRESSED_NII_FILENAME:str, DATA: npt.NDArray[np.float64], my_data_labels_which_are_a_guess, my_colors, MY_DATA_THRESHOLD:float = 0.1e0)->int:
    if(not the_delaunay_of_the_mesh_was_successful(COMPRESSED_NII_FILENAME, DATA, my_data_labels_which_are_a_guess, my_colors)):
        return 1
    return 0

def plot_individual_regions(file_i_used_for_validation, my_guesses_about_the_labels, my_colors):
    return plot_if_delaunay_was_a_success(file_i_used_for_validation, nib.load(file_i_used_for_validation).get_fdata(), my_guesses_about_the_labels, my_colors)

def plot_entire_tumor(validation_data, validation_data_lables, colors)->None:
    return compute_the_delaunay(validation_data, nib.load(validation_data).get_fdata(), validation_data_lables, colors)

def main()->int:
    my_guesses_about_the_labels:list[str] = ['peritumoral edema/infiltrating tissue', 'necrotic tumor core', 'GD-enhanced tumor']
    my_colors = ["green", "red", "yellow"]

    #file_i_used_for_prediction:str = '../output_tumor/unetr_pp/3d_fullres/Task003_tumor/unetr_pp_trainer_tumor__unetr_pp_Plansv2.1/fold_0/validation_raw_postprocessed/BRATS_397.nii.gz'
    file_i_used_for_validation:str = '../output_tumor/unetr_pp/3d_fullres/Task003_tumor/unetr_pp_trainer_tumor__unetr_pp_Plansv2.1/gt_niftis/BRATS_397.nii.gz'

    #plot_individual_regions(file_i_used_for_validation, my_guesses_about_the_labels, my_colors)
    plot_entire_tumor(file_i_used_for_validation, my_guesses_about_the_labels, my_colors)

    return 0


if('__main__' == __name__):
    main()
