import os
import threading
from tkinter import *
import tkinter.ttk as ttk
from main_process import create_csv_for_machine_learning
from predict_traits_score import predict_traits_on_new_data
import numpy as np


data_folder = ''
predicted_traits_file_name = ''


def predict_traits():
    """
    predict the traits values of the requested candidates
    :return: the path to the predicted results
    """
    final_ml_data_path = r'C:\Users\onaki\CyberTraits\cyberTraits\final\final_models'
    # {{trait1: [y predicted lists for all the candidates],
    #   trait2: [y predicted lists for all the candidates], ... ,
    #   traitN: [y predicted lists for all the candidates]}
    candidates_list, predicted_values_dic = predict_traits_on_new_data(final_ml_data_path)

    # print the results of the prediction
    predicted_traits_file = 'predicted_traits.csv'
    titles_list = ['candidate_id'] + list(predicted_values_dic)
    predicted_traits_list = []
    # pass on every candidate
    for i, candidate in enumerate(candidates_list):
        curr_candidate_traits_scores_list = [candidate]
        # pass on every trait
        for trait, trait_scores in predicted_values_dic.items():
            curr_candidate_traits_scores_list.append(trait_scores[i])
        predicted_traits_list.append(curr_candidate_traits_scores_list)
    predicted_traits_list.insert(0, titles_list)
    np.savetxt(predicted_traits_file, np.array(predicted_traits_list), delimiter=',', fmt='%s')
    return predicted_traits_file


def organize_predict_traits():
    """
    send to the data to the organization function and to the prediction function,
    in the end, update the global variable with the results file name
    """
    data_folder_n = os.path.normpath(data_folder)
    # create the csv file for machine learning
    create_csv_for_machine_learning(data_folder_n, is_research=False)
    # predict the traits scores
    global predicted_traits_file_name
    predicted_traits_file_name = predict_traits()


def organize_predict_clicked():
    """
    start the progressbar, disable the buttons and start the thread of predicting the data
    """
    progressbar.grid(row=1, sticky=W, padx=5, pady=5)
    wait_lbl.grid(row=2)
    enter_path_btn.config(state="disabled")
    organize_predict_data_btn.config(state="disabled")
    # defining the thread
    global submit_thread
    submit_thread = threading.Thread(target=organize_predict_traits)
    submit_thread.daemon = True
    progressbar.start()
    submit_thread.start()
    # check if the thread finished
    root.after(20, check_thread_finished)


def check_thread_finished():
    """
    check if the thread of predicting the data finished, and if yes -> handling the next steps
    """
    if submit_thread.is_alive():
        # if the thread is still alive -> check again after a while
        root.after(20, check_thread_finished)
    else:
        # the thread finished -> stopping the progressbar and printing the results file path
        progressbar.stop()
        wait_lbl.grid_forget()
        progressbar.grid_forget()
        predicted_done_lbl.grid(row=4)
        predicted_done_lbl['text'] = 'Predicted Done.\nResults found in file:\n' + \
                                     os.path.join(os.path.abspath(os.getcwd()), predicted_traits_file_name)
        # delete the previous dir path
        path_txt.delete(0, END)
        # enable the buttons
        enter_path_btn.config(state="normal")
        organize_predict_data_btn.config(state="normal")
        # hide the "organize and predict" button
        organize_predict_data_btn.grid_forget()


def folder_path_clicked():
    """
    handle the button "enter path"
    """
    global data_folder
    data_folder = path_txt.get()
    predicted_done_lbl.grid_forget()
    if not os.path.isdir(data_folder):
        error_path_lbl.grid(column=2, row=0)
        error_path_lbl.configure(text='Path not found, Please enter another one')
        organize_predict_data_btn.grid_forget()
    else:
        error_path_lbl.grid_forget()
        organize_predict_data_btn.grid(row=0, sticky=E)


################# the tkinter main loop #################
root = Tk()
root.title("Welcome to Cyber Traits - Traits Prediction Program")
root.geometry('1000x400')
root.grid()

# the label that asking to enter the path data
enter_path_lbl = Label(root, text="Enter full path to data folder:", font=("Arial Bold", 14), justify=LEFT,
                       padx=15, pady=15)
enter_path_lbl.grid(column=0, row=0)

# the text to enter the path in it
path_txt = Entry(root, width=50)
path_txt.grid(column=1, row=0)

# the button of entering the path
enter_path_btn = Button(root, text="Enter Path", command=folder_path_clicked, justify=LEFT,
                        padx=10, pady=10)
enter_path_btn.grid(column=0, row=1)

# the label of the error path
error_path_lbl = Label(root, text="Path not found, Please enter another one", font=("Arial Bold", 10),
                       justify=LEFT, bg='red', padx=5, pady=5)

# a frame that will contain variables
frame = ttk.Frame(root)
frame.grid(column=0, row=2, padx=10, pady=10)

# the button of predicting the data
organize_predict_data_btn = Button(frame, text="Organize and Predict Data", command=organize_predict_clicked,
                                   justify=CENTER, padx=5, pady=5)

# the progress bar, that moving when the program organize and calculate the data
progressbar = ttk.Progressbar(frame, mode='indeterminate')

# the label that says the program is in middle to process the data
wait_lbl = Label(frame, text="Processing, please wait..", padx=5, pady=5)

# the label that says that the predict finished, and gives the user the path to the results file
predicted_done_lbl = Label(frame, text='', font=("Arial Bold", 10), justify=LEFT, padx=5, pady=5, bg='green')

root.mainloop()

'''
from tkinter import *
from tkinter.ttk import *
from useful_functions import *
from main_process import create_csv_for_machine_learning
from predict_traits_score import predict_traits_on_new_data
import multiprocessing
import time
import numpy as np

data_folder = ''

prediction_done = True


# Function responsible for the updation
# of the progress bar value
def darw_bar():
    while not prediction_done:
        progress['value'] = 0
        window.update_idletasks()
        #time.sleep(0.5)

        progress['value'] = 20
        window.update_idletasks()
        #time.sleep(0.5)

        progress['value'] = 40
        window.update_idletasks()
        #time.sleep(0.5)

        progress['value'] = 50
        window.update_idletasks()
        #time.sleep(0.5)

        progress['value'] = 60
        window.update_idletasks()
        #time.sleep(0.5)

        progress['value'] = 80
        window.update_idletasks()
        #time.sleep(0.5)

        progress['value'] = 100


def folder_path_clicked():
    """
    handle the button "enter path"
    """
    global data_folder
    data_folder = path_txt.get()
    predicted_done_lbl.grid_forget()
    if not os.path.isdir(data_folder):
        error_path_lbl.grid(column=2, row=0)
        error_path_lbl.configure(text='Path not found, Please enter another one')
        organize_predict_data_btn.grid_forget()
    else:
        error_path_lbl.grid_forget()
        organize_predict_data_btn.grid(column=0, row=2)


def organize_predict_data():
    """
    send the data for organization and prediction
    :return: the predicted file path
    """
    print('hellloooo')
    data_folder_n = os.path.normpath(data_folder)
    # create the csv file for machine learning
    print('hellloooo----')
    create_csv_for_machine_learning(data_folder_n, is_research=False)
    # predict the traits scores
    print('hellloooo--------')
    predicted_traits_file = predict_traits()

    return predicted_traits_file

def organize_predict_clicked():
    """
    handle the button "organize and predict data"
    """
    wait_lbl.grid(column=2, row=2)
    progress.grid(column=1, row=2)

    global prediction_done
    prediction_done = False

    # start to fulfill the progress bar
    darw_bar()

    # send the data for organization and prediction
    organize_predict_data()

    draw_bar_p = multiprocessing.Process(name='my_service', target=darw_bar)
    organize_predict_data_p = multiprocessing.Process(name='worker 1', target=organize_predict_data)

    organize_predict_data_p.start()
    draw_bar_p.start()


    wait_lbl.grid_forget()
    progress.grid_forget()

    predicted_done_lbl.grid(column=0, row=3)
    predicted_done_lbl['text'] = 'Predicted Done.\nResults found in file:\n' + \
                                 os.path.join(os.path.abspath(os.getcwd()), predicted_traits_file)


def predict_traits():
    """
    predict the traits values of the requested candidates
    :return: the path to the predicted results
    """
    final_ml_data_path = 
    # {{trait1: [y predicted lists for all the candidates],
    #   trait2: [y predicted lists for all the candidates], ... ,
    #   traitN: [y predicted lists for all the candidates]}
    candidates_list, predicted_values_dic = predict_traits_on_new_data(final_ml_data_path)

    # print the results of the prediction
    predicted_traits_file = 'predicted_traits.csv'
    titles_list = ['candidate_id'] + list(predicted_values_dic)
    predicted_traits_list = []
    # pass on every candidate
    for i, candidate in enumerate(candidates_list):
        curr_candidate_traits_scores_list = [candidate]
        # pass on every trait
        for trait, trait_scores in predicted_values_dic.items():
            curr_candidate_traits_scores_list.append(trait_scores[i])
        predicted_traits_list.append(curr_candidate_traits_scores_list)
    predicted_traits_list.insert(0, titles_list)
    np.savetxt(predicted_traits_file, np.array(predicted_traits_list), delimiter=',', fmt='%s')
    # finished to predict
    global prediction_done
    prediction_done = True
    return predicted_traits_file


window = Tk()
window.title("Welcome to Cyber Traits app")
window.geometry('1000x400')

enter_path_lbl = Label(window, text="Enter full path to data folder", font=("Arial Bold", 14))
enter_path_lbl.grid(column=0, row=0)

error_path_lbl = Label(window, text="Path not found, Please enter another one", font=("Arial Bold", 12))#, bg='red')

path_txt = Entry(window, width=50)
path_txt.grid(column=1, row=0)

enter_path_btn = Button(window, text="Enter Path", command=folder_path_clicked)
enter_path_btn.grid(column=0, row=1)

organize_predict_data_btn = Button(window, text="Organize and Predict Data", command=organize_predict_clicked)

predicted_done_lbl = Label(window, text='', font=("Arial Bold", 10))
wait_lbl = Label(window, text="Processing, please wait..")
# Progress bar widget
progress = Progressbar(window, orient=HORIZONTAL, length=100, mode='indeterminate')

window.mainloop()
'''
