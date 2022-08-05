# Controller Implementations Under Timing Uncertainties

The tool is based on the following work:

**Safety Analysis of Embedded Controllers under Implementation Platform Timing Uncertainties**. Clara Hobbs, Bineet Ghosh, Shengjie Xu, Parasara Sridhar Duggirala, Samarjit Chakraborty. In: EMSOFT. 2022. *(To appear)*.

This code is to compute the maximum deviation using the following two methods:

* Uncertain Linear Systems (Algorithm 1) (`ULSBased`).
* Generalized Recurrence Relations (Algorithm 2) (`FSMBased`).

## Installation

### Dependencies

- [`Python 3.9.x`](https://www.python.org/)
- [`NumPy`](https://numpy.org/)
- [`SciPy`](https://scipy.org/)
- [`mpmath`](https://mpmath.org/)
- Gurobi Python Interface:
  - Please obtain appropriate Gurobi License from [here](http://www.gurobi.com/downloads/licenses/license-center). Please refer to this [link](https://www.gurobi.com/documentation/8.1/quickstart_windows/academic_validation.html) for details. After the license is installed properly, Gurobi can be used from home network.
  - Install Gurobi. Please note that we will need Gurobi Python Interface: 
    - On-line documentation on installation can be found [here](http://www.gurobi.com/documentation/).
    - **[Recommend]** Gurobi Python Interface can also be installed through [Anaconda](https://www.anaconda.com/). Details on installing Gurobi Python Interface through `conda` can be found [here](https://www.gurobi.com/documentation/8.1/quickstart_mac/installing_the_anaconda_py.html#section:Anaconda).

### Downloading 

1. Download the repository to your desired location `/my/location/`:

   * ```shell
     git clone https://github.com/bineet-coderep/Jittery-Scheduler.git
     ```

2. Once the repository is downloaded, please open `~/.bashrc`, and add the line `export SCHDLR_ROOT_DIR=/my/location/Jittery-Scheduler/`, mentioned in the following steps:

   * ```shell
     vi ~/.baschrc
     ```

3. Once `.bashrc` is opened, please add the location, where the tool was downloaded, to a path variable `MNTR_ROOT_DIR` (This step is crucial to run the tool):

   * ```shell
     export SCHDLR_ROOT_DIR=/my/location/Jittery-Scheduler/
     ```

## Running The Tool

Once the dependencies are installed properly, and the path variable is set, following steps should run without any error.

### Case studies

We offer four case studies:

1. [RC Network](https://www.abebooks.com/servlet/SearchResults?sts=t&tn=Signals+and+Linear+Systems&x=51&y=16).
2. [Electric Steering](https://drops.dagstuhl.de/opus/volltexte/2020/12384/pdf/LIPIcs-ECRTS-2020-21.pdf).
3. [Unstable Second-Order System](https://drops.dagstuhl.de/opus/volltexte/2020/12384/pdf/LIPIcs-ECRTS-2020-21.pdf).

Here, we illustrate the Electric Steering case study, as the other one can be run in similar fashion.

1. ```shell
   cd src/
   ```

2. ```shell
   python SteeringCaseStudy.py
   ```

