FROM python:3.8-alpine

COPY index.py opt/site/ 
COPY templates opt/site/templates
COPY static opt/site/static

RUN pip install flask   

WORKDIR opt/site
ENV FLASK_APP=index.py
ENV FLASK_ENV=development
    
CMD ["flask", "run", "--host", "0.0.0.0"]