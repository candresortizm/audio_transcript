FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt --upgrade

# For local testing.
EXPOSE 5000

# Set IS_USING_IMAGE_RUNTIME Environment Variable
ENV IS_USING_IMAGE_RUNTIME=True
ENV TEMP_PATH='temp'

# Copy all files in ./src
COPY src/* ${LAMBDA_TASK_ROOT}
COPY src/app ${LAMBDA_TASK_ROOT}/app
COPY src/static ${LAMBDA_TASK_ROOT}/static
COPY src/templates ${LAMBDA_TASK_ROOT}/templates
CMD ["app.handler"]