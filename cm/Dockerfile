FROM hotmaps/base_cm:latest


# Setup app server
WORKDIR /
RUN mkdir -p /data

# Install required python modules
RUN apt-get update
RUN apt-get install python3-dev -y

COPY ./requirements.txt /cm/
RUN pip3 install -r /cm/requirements.txt

# Copy app source code
COPY . /cm
WORKDIR /cm
RUN chmod u+x /cm/wait-for-it.sh

# Compile cython files
RUN chmod u+x /cm/app/api_v1/my_calculation_module_directory/CM/helper_functions/cyf/compile_cython.sh


# Start server
EXPOSE 80

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# Start processes
CMD ["/cm/wait-for-it.sh","rabbit:5672","--strict","--timeout=360","--","/usr/bin/supervisord"]

