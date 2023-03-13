FROM includeno/pythonfirefox:3.9.16.firefox102.8.0esr

WORKDIR /app

# Copy the requirements file
ADD . /app

# Install the requirements
RUN pip install -r requirements.txt

ARG SENDER='a@126.com'
ARG PASSWORD='a@126.com'
ARG RECIPIENT='a@126.com'
ARG SMTP_SERVER='smtp.126.com'
ARG PORT=25
RUN echo ${SENDER} ${PASSWORD} ${RECIPIENT} ${SMTP_SERVER} ${PORT}

CMD python args.py --sender ${SENDER} --ps ${PASSWORD} --recipient ${RECIPIENT} --smtp_server ${SMTP_SERVER} --port ${PORT}