FROM python:3.10
USER root
WORKDIR /frontend
COPY  . /frontend/
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]