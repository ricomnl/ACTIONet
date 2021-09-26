FROM nuest/mro:4.0.2-rstudio

ENV R_REMOTES_NO_ERRORS_FROM_WARNINGS="true"
ENV DISABLE_AUTH="true"

# Install dependencies
RUN apt-get update --fix-missing && \
    apt-get install -yq libhdf5-dev libsuitesparse-dev libgit2-dev && \
    apt-get update && \
    apt-get clean && \
    apt autoremove -y


COPY files/* /tmp/
RUN mkdir /tmp/Makevars /home/$DOCKER_USER/.R && mv /tmp/Makevars /home/$DOCKER_USER/.R/Makevars && mv /tmp/Rprofile.site /opt/microsoft/ropen/4.0.2/lib64/R/etc/Rprofile.site

# Install R packages
RUN Rscript --quiet /tmp/install_actionet_deps.R
RUN Rscript --quiet /tmp/install_actionet.R

EXPOSE 8787
WORKDIR /
CMD ["/init"]