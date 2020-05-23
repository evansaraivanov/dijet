# q/g tagger calibration dijet events

Input n-tuples for sherpa and data are found in:

> /eos/user/w/wasu/AQT_dijet_sherpa_bdt/dijet_sherpa_bdt.root
> /eos/user/w/wasu/AQT_dijet_data_bdt/dijet_data_bdt.root

These are the input files for ReadingTreeMC.py and ReadingTreeData.py respectively. Run these with the following command:

> python2 root-files/ReadingTreeMC.py
> python2 root-files/ReadingTreeData.py

The outputs are root files with histograms, which are then the inputs for the other scripts.

Creating the histograms for Pythia requires extra steps. First execute writeNtuple.cxx with the following command:

> root -l root-files/writeNtuple.cxx

The output is an tree like with sherpa and data. Set the newly created file as the input for ReadingTreePyhtia.py and execute it the same way as with sherpa and data.

> python2 root-files/ReadingTreePythia.py

The other histograms that need to be created are the histograms for each pdfWeight. We would like this to be done on HTCondor, but it is a work in progress.
In the current submit file (pdf-1.sub) I copy the input file from /eos/user/w/wasu/AQT_dijet_sherpa_bdt/dijet_sherpa_bdt.root to a directory in AFS to avoid the use of the --spool option for the Condor job.
The executable is included in the base directory of this repository. It includes a shebang for the default python environment.

The issue is that the file created by the executable exceeds the max file transfer size of 1 GiB. Another issue I suddenly started having was that Condor was not copying my executable to the job directory.

To execute the condor job, use the following command:

> condor_submit pdf-1.sub

