FROM nuest/mro:4.0.2-rstudio

ENV R_REMOTES_NO_ERRORS_FROM_WARNINGS="true"
ENV DISABLE_AUTH="true"

# Install dependencies
RUN apt-get install -y libhdf5-dev libsuitesparse-dev

# Install R version 
COPY files/* /tmp/

RUN Rscript --slave /tmp/install_actionet_deps.R
RUN Rscript --slave /tmp/install_actionet.R

EXPOSE 8787
WORKDIR /
CMD ["/init"]