import boto3,csv,io,json
s3=boto3.client('s3')

def read_json_from_s3(bucket,key):
    obj=s3.get_object(Bucket=bucket,Key=key)
    return json.loads(obj['Body'].read())

def write_csv_to_s3(bucket,key,rows):
    buf=io.StringIO()
    writer=csv.writer(buf)
    for r in rows:
        writer.writerow(r)
    s3.put_object(Bucket=bucket,Key=key,Body=buf.getvalue())
