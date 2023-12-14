FROM public.ecr.aws/lambda/python:3.10
COPY . .
RUN python -m pip install -r requirements.txt
CMD ["app.handler"]