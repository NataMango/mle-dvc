import boto3


class Config:
    AWS_ACCESS_KEY_ID = 'YCAJE26tCTzKqvgfV8G9aEd-k'
    AWS_SECRET_ACCESS_KEY = 'YCO8miShSnB41jtyLQX7FRH_oz50dyFmPjEBE2uS'

    S3_SERVICE_NAME = 's3'
    S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'


def get_session():
    session = boto3.session.Session()

    return session.client(
        service_name=Config.S3_SERVICE_NAME,
        endpoint_url=Config.S3_ENDPOINT_URL,
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )

if __name__ == '__main__':
    bucket_name = 's3-student-mle-20250201-49aafe9ce5' 

    s3 = get_session()

    if s3.list_objects(Bucket=bucket_name).get('Contents'):
        for key in s3.list_objects(Bucket=bucket_name)['Contents']:
            print(key['Key'])
'''
    s3.put_object(Bucket=bucket_name, Key='example.txt', Body='Hello, World!')

    if s3.list_objects(Bucket=bucket_name).get('Contents'):
        for key in s3.list_objects(Bucket=bucket_name)['Contents']:
            print(key['Key'])
'''