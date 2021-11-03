FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
	LANG=en_US.UTF-8 LC_ALL= \
	PATH=$PATH:/opt/conda/bin

RUN apt-get update --fix-missing && \
    apt-get install -yq wget curl locales systemd screen unzip bzip2 ca-certificates pkg-config libglib2.0-0 libxext6 libsm6 libxrender1 git gdebi-core mercurial subversion cmake build-essential software-properties-common bash-completion libsuitesparse-dev libcurl4-openssl-dev libssl-dev libxml2-dev libhdf5-dev libnss3 xvfb && \
    add-apt-repository ppa:cran/libgit2 && \
    apt-get update && \
    apt-get clean && \
    apt autoremove -y

RUN  ln -s /bin/tar /bin/gtar

#download the latest anaconda 
COPY files/base_environment.yml /tmp/base_environment.yml
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
	conda install mamba -n base -c conda-forge  && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    mamba update --quiet --yes conda && \
	mamba update --quiet --yes mamba && \
    mamba env update -f /tmp/base_environment.yml -n base && \
    jupyter notebook --generate-config && \
    mamba clean --all -ftipsy && \
    rm -rf ~/.cache/pip
    
##Copy config file
COPY files/jupyter_notebook_config.py /home/$DOCKER_USER/.jupyter/jupyter_notebook_config.py
COPY files/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# We aren't running a GUI, so force matplotlib to use
# the non-interactive "Agg" backend for graphics.
# Run matplotlib once to build the font cache.
ENV MATPLOTLIBRC=/home/$DOCKER_USER/.config/matplotlib/matplotlibrc
RUN mkdir -p /home/$DOCKER_USER/.config/matplotlib && \
    echo "backend      : Agg" > /home/$DOCKER_USER/.config/matplotlib/matplotlibrc && \
    python -c "import matplotlib.pyplot"

# Instruct joblib to use disk for temporary files. Joblib defaults to
# /shm when that directory is present. In the Docker container, /shm is
# present but defaults to 64 MB.
# https://github.com/joblib/joblib/blob/0.11/joblib/parallel.py#L328L342
ENV JOBLIB_TEMP_FOLDER=/tmp
ENV PATH=$PATH:/opt/conda/bin \
    CONDARC=/opt/conda/.condarc \
    CONDA_DIR=/opt/conda

# Install python actionet 
RUN pip install git+https://github.com/shmohammadi86/ACTIONet@python-release

#create an R conda environment
# COPY files/r_environment.yml /tmp
# RUN mamba env update -f /tmp/r_environment.yml --name r_env && \    
#     mamba clean --all -f -y && \
#     rm -rf ~/.cache/pip

# ENV R_HOME=/opt/conda/envs/r_env/lib/R \
# 	CRAN=https://cloud.r-project.org

# Install R
RUN echo "## R 4.X \
    deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/ \
    deb-src https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" >> /etc/apt/sources.list $$ \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
    apt update && \
    apt install r-base -y

ENV R_HOME=/usr/local/lib/R \
	CRAN=https://cloud.r-project.org
    
RUN mkdir -p ${R_HOME}/site-library && \
	chown root:staff ${R_HOME}/site-library && \
	chmod g+ws ${R_HOME}/site-library && \
    mkdir -p ${R_HOME}/etc && \
	echo "R_LIBS=\${R_LIBS-'${R_HOME}/site-library:${R_HOME}/library'}" >> ${R_HOME}/etc/Renviron && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_US.utf8 && \
    /usr/sbin/update-locale LANG=en_US.UTF-8

COPY files/*R /tmp/
# Install R kernel 
RUN Rscript /tmp/install_irkernel.R
# Install R actionet
RUN Rscript /tmp/install_actionet_deps.R
RUN Rscript /tmp/install_actionet.R 

# Install RStudio
ENV RSTUDIO_VERSION=2021.09.0+351
ENV S6_VERSION=v2.1.0.2
ENV PATH=/usr/lib/rstudio-server/bin:$PATH
ENV RSTUDIO_URL="http://download2.rstudio.org/server/bionic/amd64/rstudio-server-${RSTUDIO_VERSION}-amd64.deb"

WORKDIR /rocker_scripts
ADD https://raw.githubusercontent.com/rocker-org/rocker-versioned2/master/scripts/install_rstudio.sh install_rstudio.sh
ADD https://raw.githubusercontent.com/rocker-org/rocker-versioned2/master/scripts/install_pandoc.sh install_pandoc.sh
ADD https://raw.githubusercontent.com/rocker-org/rocker-versioned2/master/scripts/install_s6init.sh install_s6init.sh
ADD https://raw.githubusercontent.com/rocker-org/rocker-versioned2/master/scripts/default_user.sh default_user.sh
ADD https://raw.githubusercontent.com/rocker-org/rocker-versioned2/master/scripts/userconf.sh userconf.sh
ADD https://raw.githubusercontent.com/rocker-org/rocker-versioned2/master/scripts/pam-helper.sh pam-helper.sh

RUN chmod +x *.sh && \
  ./install_rstudio.sh && \
  ./install_pandoc.sh

RUN mv /init /init-rstudio

# Start container
RUN mkdir /data && chmod -R 777 /data
WORKDIR /data
EXPOSE 1-65535
# CMD jupyter-lab --ip=0.0.0.0 --no-browser --allow-root --LabApp.token=''
CMD screen -d -m bash -c "jupyter-lab --ip=0.0.0.0 --no-browser --allow-root --LabApp.token=''" && /init-rstudio
