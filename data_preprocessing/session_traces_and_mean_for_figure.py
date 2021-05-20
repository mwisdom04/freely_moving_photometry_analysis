import pickle
import os
from utils.individual_trial_analysis_utils import SessionData
import pandas as pd
from data_preprocessing.session_traces_and_mean import get_all_experimental_records
from utils.post_processing_utils import remove_exps_after_manipulations, remove_bad_recordings
from utils.regression.linear_regression_utils import get_first_x_sessions

def add_experiment_to_aligned_data(experiments_to_add):
    data_root = r'W:\photometry_2AC\processed_data\for_figure'
    for index, experiment in experiments_to_add.iterrows():
        print(experiment['mouse_id'],' ', experiment['date'])
        saving_folder = os.path.join(data_root, experiment['mouse_id'])
        if not os.path.exists(saving_folder):
            os.makedirs(saving_folder)

        session_traces = SessionData(experiment['fiber_side'], experiment['recording_site'], experiment['mouse_id'], experiment['date'])
        session_traces.get_choice_responses()
        session_traces.get_cue_responses()
        session_traces.get_reward_responses()
        session_traces.get_outcome_responses()
        aligned_filename = experiment['mouse_id'] + '_' + experiment['date'] + '_' + 'aligned_traces_for_fig.p'
        save_filename = os.path.join(saving_folder, aligned_filename)
        pickle.dump(session_traces, open(save_filename, "wb"))


if __name__ == '__main__':
    mouse_ids = ['SNL_photo28', 'SNL_photo30', 'SNL_photo31', 'SNL_photo32', 'SNL_photo33', 'SNL_photo34', 'SNL_photo35']
    site = 'Nacc'
    experiment_record = pd.read_csv('W:\\photometry_2AC\\experimental_record.csv')
    experiment_record['date'] = experiment_record['date'].astype(str)
    clean_experiments = remove_exps_after_manipulations(experiment_record, mouse_ids)
    all_experiments_to_process = clean_experiments[
        (clean_experiments['mouse_id'].isin(mouse_ids)) & (clean_experiments['recording_site'] == site)].reset_index(
        drop=True)
    experiments_to_process = get_first_x_sessions(all_experiments_to_process)
    add_experiment_to_aligned_data(experiments_to_process)
    # date = '20201119'
    # for mouse_id in mouse_ids:
    #     all_experiments = get_all_experimental_records()
    #
    #     if (mouse_id =='all') & (date == 'all'):
    #         experiments_to_process = all_experiments
    #     elif (mouse_id == 'all') & (date != 'all'):
    #         experiments_to_process = all_experiments[all_experiments['date'] == date]
    #     elif (mouse_id != 'all') & (date == 'all'):
    #         experiments_to_process = all_experiments[all_experiments['mouse_id'] == mouse_id]
    #     elif (mouse_id != 'all') & (date != 'all'):
    #         experiments_to_process = all_experiments[(all_experiments['date'] == date) & (all_experiments['mouse_id'] == mouse_id)]
    #     add_experiment_to_aligned_data(experiments_to_process)

