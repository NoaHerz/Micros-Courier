from glob import glob
import numpy as np
from os import path

def define_data(micros,dBoy25,DBoy3_1,include_learning, DBoy4):

    # micros: if set to True include only subjects with microwire data

    basepath = '/data/events/courier/'

    sessionList = []
    if dBoy25:
        sessionList.extend(np.array(glob(basepath+'dBoy25/processed/*.mat')).tolist())
    if DBoy3_1:
        sessionList.extend(np.array(glob(basepath+'DBoy3_1/delivery/processed/*.mat')).tolist())
        if include_learning:
            sessionList.extend(np.array(glob(basepath+'DBoy3_1/learning/processed/*.mat')).tolist())
    if DBoy4:
        sessionList.extend(np.array(glob(basepath+'DBoy4/processed/*.mat')).tolist())

    subjectList = np.unique([sessi.split('/')[-1][:sessi.split('/')[-1].find('_e')] for sessi in sessionList]).tolist()

    # Optionally filter out sessions without microelectrode recordings
    if micros:
        noMicros = [subi for subi in subjectList if not path.exists('/data/eeg/'+subi+'/npt')
                and not path.exists('/data/eeg/'+subi+'/spikes')
                and not path.exists('/data/eeg/'+subi+'/wave_clus')
                and not path.exists('/data/eeg/'+subi+'/raw/microeeg')
                and not path.exists('/data/eeg/'+subi+'/raw/micro')
                and not path.exists('/data/eeg/'+subi+'/micro')
                and len(glob('/data/eeg/'+subi+'/raw/*/micro')) == 0
                and len(glob('/data/eeg/'+subi+'/raw/*/*/nlx')) == 0
                and len(glob('/data/eeg/'+subi+'/*/*/*/*/*.ncs')+glob('/data/eeg/'+subi+'/*/*/*/*.ncs')+glob('/data/eeg/'+subi+'/*/*/*.ncs')) == 0
                and len(glob('/data/eeg/'+subi+'/raw/*.emg')) == 0 ]
        print('noMicros')
        print(noMicros)
        exc_subs_micro = ['FR423', 'FR424','FR460', 'TJ039', 'TJ005_1', 'R1068J','R1017J','TJ027','R1019J','R1030J']#TJ027 wire bundles in WM, R1017J wires can not be mapped to leads >> no locs, R1019J not aligned, R1030J not aligned, 'FR460' strong artifact on multiple wires
        subjectList = [subi for subi in subjectList if subi not in noMicros and subi not in exc_subs_micro]#FR423 no splitted sync files; 424 no splitted files; TJ039, TJ005_1 no nlx data for dperson; R1068J  does not align;
        sessionList = [sessi for sessi in sessionList for subi in subjectList if subi+'_e' in sessi and subi not in exc_subs_micro and 'FR436_events_sess1' not in sessi and 'FR463_events_sess2' not in sessi and 'FR463_events_sess1' not in sessi and 'FR426_events_sess1' not in sessi  ]#'FR436_events_sess1' no micro data

    subjectList.sort()
    sessionList.sort()

    return(subjectList,sessionList)
