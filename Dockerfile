FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN yum update -y && \
    yum install -y mesa-libGL

COPY . ${LAMBDA_TASK_ROOT}

CMD ["app.lambda_handler"]
