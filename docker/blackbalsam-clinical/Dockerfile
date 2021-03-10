FROM helxplatform/blackbalsam:py3.7-v0.0.15

USER root

COPY ./r-packages.txt .
RUN conda install --quiet --yes --file r-packages.txt && \
        conda clean --all -f -y && \
        fix-permissions $CONDA_DIR && \
        fix-permissions /home/$NB_USER
RUN R -e 'install.packages(c("ggplot2", "ggimage", "geex", "tableone"), repos = "http://cran.us.r-project.org")'
RUN chown -R 1000:0 /home/$NB_USER
RUN chmod -R g+w /home/$NB_USER
