FROM python:slim

COPY ./ /home/scraper

WORKDIR /home/scraper

RUN pip install -r requirements.txt --src /home/scraper

EXPOSE 5000

CMD ["python", "run.py"]